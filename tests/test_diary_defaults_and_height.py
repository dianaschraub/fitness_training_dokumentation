"""Exercise widget/session transitions without Google credentials."""
import ast
from pathlib import Path
import unittest
from unittest.mock import Mock


SOURCE = Path(__file__).resolve().parents[1] / "streamlit_app.py"


class Rerun(BaseException):
    pass


class State(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


class UI:
    def __init__(self, state, pressed=None, height=None):
        self.session_state = state
        self.pressed = pressed
        self.number_input = Mock(return_value=height)
        self.caption = Mock()
        self.error = Mock()

    def button(self, label, *, key, disabled=False, **kwargs):
        return key == self.pressed and not disabled

    def rerun(self):
        raise Rerun()


def compile_blocks():
    tree = ast.parse(SOURCE.read_text())
    opening = next(
        node for node in ast.walk(tree)
        if isinstance(node, ast.If)
        and isinstance(node.test, ast.Call)
        and any(kw.arg == "key" and isinstance(kw.value, ast.Constant)
                and kw.value.value == "btn_create"
                for kw in node.test.keywords)
    )
    height_assignment = next(
        node for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "gespeicherte_groesse"
                for t in node.targets)
    )
    height_if = next(
        node for node in ast.walk(tree)
        if isinstance(node, ast.If)
        and ast.unparse(node.test).startswith("gespeicherte_groesse is None")
    )
    def compile_nodes(nodes):
        return compile(ast.Module(body=nodes, type_ignores=[]), str(SOURCE), "exec")
    return compile_nodes([opening]), compile_nodes([height_assignment, height_if])


OPENING, HEIGHT = compile_blocks()


class DiaryDefaultsAndHeightTests(unittest.TestCase):
    def run_height(self, state, pressed=None, value=None, write=None):
        ui = UI(state, pressed, value)
        writer = write if write is not None else Mock()
        try:
            exec(HEIGHT, {"st": ui, "_speichere_koerpergroesse": writer})
        except Rerun:
            pass
        return ui, writer

    def test_each_today_and_week_category_overrides_old_selection(self):
        for scope in ("heute", "woche"):
            for category in ("Ausdauer", "Kraft", "Beweglichkeit", "Balance",
                             "Ernährung", "Gesamtbefinden"):
                with self.subTest(scope=scope, category=category):
                    state = State(detail_ansicht=(scope, category),
                                  entry_kategorie="Ausdauer")
                    ui = UI(state, "btn_create")
                    with self.assertRaises(Rerun):
                        exec(OPENING, {"st": ui})
                    self.assertEqual(state.entry_kategorie, category)
                    self.assertTrue(state.eintrag_modal_aktiv)

    def test_dialog_changes_are_not_overridden_without_opening(self):
        state = State(detail_ansicht=("heute", "Balance"),
                      entry_kategorie="Kraft")
        exec(OPENING, {"st": UI(state)})
        self.assertEqual(state.entry_kategorie, "Kraft")

    def test_opening_without_category_keeps_existing_default(self):
        state = State(entry_kategorie="Ausdauer")
        with self.assertRaises(Rerun):
            exec(OPENING, {"st": UI(state, "btn_create")})
        self.assertEqual(state.entry_kategorie, "Ausdauer")

    def test_saved_height_has_no_input(self):
        ui, writer = self.run_height(State(koerpergroesse_cm=165.0))
        ui.number_input.assert_not_called()
        ui.caption.assert_called_once_with("Körpergröße: 165 cm")
        writer.assert_not_called()

    def test_first_save_hides_input_on_next_render(self):
        state = State(koerpergroesse_cm=None)
        ui, writer = self.run_height(state, "groesse_speichern", 170.0)
        writer.assert_called_once_with(170.0)
        self.assertEqual(state.koerpergroesse_cm, 170.0)
        self.assertFalse(state.groesse_bearbeiten)
        next_ui, _ = self.run_height(state)
        next_ui.number_input.assert_not_called()

    def test_change_then_save_uses_old_height_until_write_succeeds(self):
        state = State(koerpergroesse_cm=165.0)
        self.run_height(state, "groesse_aendern")
        self.assertTrue(state.groesse_bearbeiten)
        self.assertEqual(state.groesse_input, 165.0)
        def write(value):
            self.assertEqual(state.koerpergroesse_cm, 165.0)
        self.run_height(state, "groesse_speichern", 166.0, Mock(side_effect=write))
        self.assertEqual(state.koerpergroesse_cm, 166.0)
        self.assertFalse(state.groesse_bearbeiten)

    def test_failure_keeps_previous_height_and_editor(self):
        state = State(koerpergroesse_cm=165.0, groesse_bearbeiten=True)
        ui, _ = self.run_height(
            state, "groesse_speichern", 166.0,
            Mock(side_effect=RuntimeError("offline")))
        self.assertEqual(state.koerpergroesse_cm, 165.0)
        self.assertTrue(state.groesse_bearbeiten)
        ui.error.assert_called_once()

    def test_cancel_keeps_saved_height_without_writing(self):
        state = State(koerpergroesse_cm=165.0, groesse_bearbeiten=True)
        _, writer = self.run_height(state, "groesse_abbrechen", 166.0)
        self.assertEqual(state.koerpergroesse_cm, 165.0)
        self.assertFalse(state.groesse_bearbeiten)
        writer.assert_not_called()

    def test_empty_height_cannot_be_saved(self):
        state = State(koerpergroesse_cm=None)
        _, writer = self.run_height(state, "groesse_speichern")
        writer.assert_not_called()
        self.assertIsNone(state.koerpergroesse_cm)


if __name__ == "__main__":
    unittest.main()
