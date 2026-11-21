"""Prepare measured vital signs and a shared Vega-Lite comparison."""
import math
import pandas as pd


VITAL_EINHEITEN = {
    "Schritte": "Schritte",
    "Gewicht": "kg",
    "VO₂max": "ml/kg/min",
    "BMI": "kg/m²",
}
VITAL_FARBEN = ["#496f59", "#496b89", "#a15f47", "#76618d"]


def vital_verlaufsdaten(daten, groesse_cm=None):
    """Use the last valid measurement per day; never fill missing days."""
    columns = ["Datum", "Messgröße", "Wert", "Einheit"]
    if daten.empty or "Datum" not in daten:
        return pd.DataFrame(columns=columns)
    daily = daten.copy()
    daily["Datum"] = pd.to_datetime(daily["Datum"], errors="coerce").dt.normalize()
    daily = daily.dropna(subset=["Datum"])
    for name in ("Schritte", "Gewicht", "VO2max"):
        if name not in daily:
            daily[name] = float("nan")
        values = pd.to_numeric(daily[name], errors="coerce")
        values = values.replace([float("inf"), -float("inf")], float("nan"))
        daily[name] = values.where(values >= 0 if name == "Schritte" else values > 0)
    daily = daily.groupby("Datum", as_index=False, sort=True)[
        ["Schritte", "Gewicht", "VO2max"]
    ].last().rename(columns={"VO2max": "VO₂max"})
    try:
        height = float(groesse_cm)
    except (TypeError, ValueError):
        height = float("nan")
    daily["BMI"] = (
        daily["Gewicht"] / (height / 100) ** 2
        if math.isfinite(height) and height > 0 else float("nan")
    )
    values = daily.melt(
        id_vars="Datum", value_vars=list(VITAL_EINHEITEN),
        var_name="Messgröße", value_name="Wert",
    ).dropna(subset=["Wert"])
    values["Einheit"] = values["Messgröße"].map(VITAL_EINHEITEN)
    return values[columns].reset_index(drop=True)


def _messwert_text(value, name):
    text = (
        f"{value:,.0f}".replace(",", ".") if name == "Schritte"
        else f"{value:.1f}".replace(".", ",")
    )
    return f"{text} {VITAL_EINHEITEN[name]}"


def vital_vergleichsdaten(werte):
    """0% refers to each series' first positive value in the selected period."""
    parts = []
    for name in VITAL_EINHEITEN:
        group = werte[werte["Messgröße"] == name].sort_values("Datum")
        positive = group[group["Wert"] > 0]
        if positive.empty:
            continue
        reference = positive.iloc[0]
        group = group.copy()
        group["Aenderung"] = (group["Wert"] / reference["Wert"] - 1) * 100
        group["Messwert"] = group["Wert"].map(lambda v: _messwert_text(v, name))
        group["AenderungText"] = group["Aenderung"].map(
            lambda v: f"{v:+.1f} %".replace(".", ","))
        group["Referenzwert"] = _messwert_text(reference["Wert"], name)
        group["Referenzdatum"] = reference["Datum"]
        parts.append(group)
    if not parts:
        return pd.DataFrame(columns=[
            *werte.columns, "Aenderung", "Messwert", "AenderungText",
            "Referenzwert", "Referenzdatum",
        ])
    return pd.concat(parts, ignore_index=True)


def vital_vergleich_spec(vergleich):
    """Interactive common scale, original-value tooltips, selectable legend."""
    values = vergleich.copy()
    for name in ("Datum", "Referenzdatum"):
        values[name] = pd.to_datetime(values[name]).dt.strftime("%Y-%m-%d")
    names = list(VITAL_EINHEITEN)
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "height": 320,
        "data": {"values": values.to_dict("records")},
        "layer": [
            {
                "data": {"values": [{}]},
                "mark": {"type": "rule", "color": "#b9c7bd", "strokeDash": [3, 3]},
                "encoding": {"y": {"datum": 0, "type": "quantitative"}},
            },
            {
                "params": [{
                    "name": "vital_auswahl",
                    "select": {"type": "point", "fields": ["Messgröße"], "toggle": True},
                    "bind": "legend",
                }],
                "transform": [{"filter": {"param": "vital_auswahl", "empty": True}}],
                "mark": {
                    "type": "line", "strokeWidth": 2.5,
                    "point": {"filled": True, "size": 45},
                },
                "encoding": {
                    "x": {
                        "field": "Datum", "type": "temporal", "title": None,
                        "axis": {"format": "%d.%m.", "labelOverlap": True},
                    },
                    "y": {
                        "field": "Aenderung", "type": "quantitative",
                        "title": "Veränderung (%)", "scale": {"zero": True},
                    },
                    "color": {
                        "field": "Messgröße", "type": "nominal",
                        "scale": {"domain": names, "range": VITAL_FARBEN},
                        "legend": {"title": None, "orient": "top", "columns": 2},
                    },
                    "strokeDash": {
                        "field": "Messgröße", "type": "nominal",
                        "scale": {
                            "domain": names,
                            "range": [[1, 0], [1, 0], [1, 0], [6, 3]],
                        },
                        "legend": None,
                    },
                    "order": {"field": "Datum", "type": "temporal"},
                    "tooltip": [
                        {"field": "Datum", "type": "temporal",
                         "title": "Datum", "format": "%d.%m.%Y"},
                        {"field": "Messgröße", "type": "nominal"},
                        {"field": "Messwert", "type": "nominal"},
                        {"field": "AenderungText", "type": "nominal",
                         "title": "Veränderung"},
                        {"field": "Referenzwert", "type": "nominal",
                         "title": "Startwert"},
                        {"field": "Referenzdatum", "type": "temporal",
                         "title": "Startdatum", "format": "%d.%m.%Y"},
                    ],
                },
            },
        ],
        "config": {
            "background": "transparent",
            "axis": {
                "labelColor": "#4f5e57", "titleColor": "#4f5e57",
                "labelFontSize": 11, "domainColor": "#cbd5ce",
                "tickColor": "#cbd5ce", "gridColor": "#e4e9e4",
            },
            "legend": {"labelColor": "#293b32"},
            "view": {"stroke": None},
        },
    }
