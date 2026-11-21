import json
from pathlib import Path
import sys
import unittest

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from vital_charts import (
    VITAL_EINHEITEN, vital_verlaufsdaten, vital_vergleichsdaten,
    vital_vergleich_spec,
)


class VitalChartsTests(unittest.TestCase):
    def sample(self):
        return pd.DataFrame([
            {"Datum": "2026-11-01", "Schritte": 5000, "Gewicht": 80,
             "VO2max": 40},
            {"Datum": "2026-11-03", "Schritte": 6000, "Gewicht": 76,
             "VO2max": 42},
        ])

    def test_all_four_metrics_and_bmi_formula(self):
        values = vital_verlaufsdaten(self.sample(), 200)
        self.assertEqual(set(values["Messgröße"]), set(VITAL_EINHEITEN))
        bmi = values[values["Messgröße"] == "BMI"]["Wert"].tolist()
        self.assertEqual(bmi, [20, 19])

    def test_percent_comparison_preserves_original_values(self):
        compared = vital_vergleichsdaten(vital_verlaufsdaten(self.sample(), 200))
        last = compared.groupby("Messgröße").last()
        self.assertAlmostEqual(last.loc["Schritte", "Aenderung"], 20)
        self.assertAlmostEqual(last.loc["Gewicht", "Aenderung"], -5)
        self.assertAlmostEqual(last.loc["VO₂max", "Aenderung"], 5)
        self.assertAlmostEqual(last.loc["BMI", "Aenderung"], -5)
        self.assertEqual(last.loc["Gewicht", "Messwert"], "76,0 kg")
        self.assertEqual(last.loc["Schritte", "Referenzwert"], "5.000 Schritte")
        self.assertTrue((compared.groupby("Messgröße").first()["Aenderung"] == 0).all())

    def test_missing_measurements_are_not_filled_or_zeroed(self):
        data = self.sample()
        data.loc[1, "VO2max"] = float("nan")
        values = vital_verlaufsdaten(data, 200)
        vo2 = values[values["Messgröße"] == "VO₂max"]
        self.assertEqual(len(vo2), 1)
        self.assertEqual(vo2.iloc[0]["Wert"], 40)
        self.assertEqual(values["Datum"].nunique(), 2)
        self.assertNotIn(pd.Timestamp("2026-11-02"), values["Datum"].tolist())

    def test_duplicate_day_uses_last_valid_value_per_metric(self):
        data = pd.DataFrame([
            {"Datum": "2026-11-01", "Schritte": 1000, "Gewicht": 80, "VO2max": 40},
            {"Datum": "2026-11-01", "Schritte": 2000, "Gewicht": None, "VO2max": 41},
        ])
        values = vital_verlaufsdaten(data, 200).set_index("Messgröße")
        self.assertEqual(len(values), 4)
        self.assertEqual(values.loc["Schritte", "Wert"], 2000)
        self.assertEqual(values.loc["Gewicht", "Wert"], 80)
        self.assertEqual(values.loc["VO₂max", "Wert"], 41)

    def test_bmi_missing_without_valid_height(self):
        for height in (None, 0, -10, float("nan"), float("inf"), "invalid"):
            with self.subTest(height=height):
                values = vital_verlaufsdaten(self.sample(), height)
                self.assertNotIn("BMI", values["Messgröße"].values)
                self.assertIn("Gewicht", values["Messgröße"].values)

    def test_zero_steps_use_first_positive_reference(self):
        data = pd.DataFrame([
            {"Datum": "2026-11-01", "Schritte": 0},
            {"Datum": "2026-11-02", "Schritte": 100},
        ])
        compared = vital_vergleichsdaten(vital_verlaufsdaten(data))
        self.assertEqual(compared["Aenderung"].tolist(), [-100, 0])
        self.assertEqual(compared["Referenzdatum"].nunique(), 1)
        self.assertEqual(compared.iloc[0]["Referenzdatum"], pd.Timestamp("2026-11-02"))

    def test_all_zero_steps_stay_in_original_data_without_fake_reference(self):
        values = vital_verlaufsdaten(pd.DataFrame([
            {"Datum": "2026-11-01", "Schritte": 0},
        ]))
        self.assertEqual(values["Wert"].tolist(), [0])
        self.assertTrue(vital_vergleichsdaten(values).empty)

    def test_legacy_missing_vo2_column(self):
        values = vital_verlaufsdaten(self.sample().drop(columns="VO2max"), 200)
        self.assertEqual(set(values["Messgröße"]), {"Schritte", "Gewicht", "BMI"})

    def test_invalid_dates_nonfinite_and_invalid_values_are_ignored(self):
        data = pd.DataFrame([
            {"Datum": "invalid", "Schritte": 100},
            {"Datum": "2026-11-01", "Schritte": -10, "Gewicht": 0, "VO2max": -1},
            {"Datum": "2026-11-02", "Schritte": float("inf"), "Gewicht": "bad"},
        ])
        self.assertTrue(vital_verlaufsdaten(data, 200).empty)

    def test_input_is_unchanged_and_single_measurements_are_supported(self):
        data = self.sample().iloc[:1].copy()
        before = data.copy(deep=True)
        compared = vital_vergleichsdaten(vital_verlaufsdaten(data, 200))
        pd.testing.assert_frame_equal(data, before)
        self.assertEqual(len(compared), 4)
        self.assertTrue((compared["Aenderung"] == 0).all())

    def test_empty_data(self):
        values = vital_verlaufsdaten(pd.DataFrame())
        self.assertTrue(values.empty)
        self.assertTrue(vital_vergleichsdaten(values).empty)

    def test_spec_is_json_serializable_and_contains_real_values(self):
        compared = vital_vergleichsdaten(vital_verlaufsdaten(self.sample(), 200))
        spec = vital_vergleich_spec(compared)
        json.dumps(spec, allow_nan=False)
        self.assertEqual(len(spec["data"]["values"]), 8)
        self.assertEqual(spec["data"]["values"][0]["Datum"], "2026-11-01")
        chart = spec["layer"][1]
        self.assertEqual(chart["params"][0]["bind"], "legend")
        self.assertEqual(chart["encoding"]["color"]["legend"]["columns"], 2)
        self.assertEqual(chart["encoding"]["strokeDash"]["scale"]["range"][-1], [6, 3])
        fields = {t["field"] for t in chart["encoding"]["tooltip"]}
        self.assertTrue({"Messwert", "Referenzwert", "Referenzdatum"}.issubset(fields))


if __name__ == "__main__":
    unittest.main()
