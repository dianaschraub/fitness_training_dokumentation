"""Run with python -m unittest discover -s tests; no Google login required."""
import ast
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock


SOURCE = Path(__file__).resolve().parents[1] / "streamlit_app.py"


class StopRun(BaseException):
    pass


class DiarySaveTests(unittest.TestCase):
    def setUp(self):
        tree = ast.parse(SOURCE.read_text())
        names = {"speichere_tagebuch", "melde_gespeichert"}
        functions = [node for node in tree.body
                     if isinstance(node, ast.FunctionDef) and node.name in names]
        self.old = object()
        self.st = SimpleNamespace(
            session_state=SimpleNamespace(protokoll=self.old),
            spinner=Mock(return_value=nullcontext()),
            error=Mock(), stop=Mock(side_effect=StopRun),
        )
        self.write = Mock()
        self.scope = {"st": self.st, "_speichere_nutzer_df": self.write,
                      "merke_ton": Mock()}
        exec(compile(ast.Module(body=functions, type_ignores=[]),
                     str(SOURCE), "exec"), self.scope)

    def test_updates_display_only_after_confirmed_write(self):
        new = object()
        def write(name, frame):
            self.assertEqual(name, "protokoll")
            self.assertIs(frame, new)
            self.assertIs(self.st.session_state.protokoll, self.old)
        self.write.side_effect = write
        self.scope["speichere_tagebuch"](new)
        self.assertIs(self.st.session_state.protokoll, new)

    def test_failure_keeps_previous_data_and_stops_success_path(self):
        self.write.side_effect = RuntimeError("offline")
        with self.assertRaises(StopRun):
            self.scope["speichere_tagebuch"](object())
        self.assertIs(self.st.session_state.protokoll, self.old)
        self.st.error.assert_called_once()

    def test_retry_writes_same_candidate_without_duplicate_local_append(self):
        new = object()
        self.write.side_effect = [RuntimeError("offline"), None]
        with self.assertRaises(StopRun):
            self.scope["speichere_tagebuch"](new)
        self.scope["speichere_tagebuch"](new)
        self.assertIs(self.st.session_state.protokoll, new)
        self.assertEqual(self.write.call_count, 2)

    def test_confirmation_survives_rerun(self):
        self.st.session_state = {}
        self.scope["melde_gespeichert"]()
        self.assertIn("gespeichert", self.st.session_state["speicher_meldung"])
        self.scope["merke_ton"].assert_called_once_with("pling")


if __name__ == "__main__":
    unittest.main()
