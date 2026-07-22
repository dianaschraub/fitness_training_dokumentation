import base64
import math
import datetime
import pandas as pd
import streamlit as st

# Seiten-Konfiguration
st.set_page_config(
    page_title="Sport-Tagebuch", page_icon="🏃‍♀️", layout="centered"
)

# --- Eigenes Icon für "Beweglichkeit" (Original-Bild des Nutzers) ---
BEWEGLICHKEIT_ICON_B64 = (
    "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"
)


def beweglichkeit_icon_html(size_px):
  """Gibt das eigene Beweglichkeit-Icon (Originalbild) als img-Tag zurück."""
  return (
      f"<img src='data:image/png;base64,{BEWEGLICHKEIT_ICON_B64}' "
      f"style='height:{size_px}px; width:{size_px}px; object-fit:contain; "
      f"vertical-align:middle;' />"
  )


def get_status_color(minutes, goal):
  """Liefert die Statusfarbe passend zur bisherigen Ampel-Logik
  (grau = nichts, rot = wenig, gelb = mittel, grün = Ziel erreicht),
  aber verhältnisbasiert, damit sie zum Ring-Füllstand passt."""
  if minutes <= 0:
    return "#c9c9c9"
  ratio = minutes / goal if goal else 0
  if ratio >= 1:
    return "#2e7d46"
  elif ratio >= 0.66:
    return "#e3a008"
  else:
    return "#d9534f"


def render_progress_ring_svg(minutes, goal, size=40, stroke_width=5):
  """Baut ein Ring-Fortschrittsdiagramm (Donut) als SVG: Füllstand
  proportional zu minutes/goal, Minutenzahl in der Mitte."""
  ratio = 0 if not goal else min(minutes / goal, 1.0)
  color = get_status_color(minutes, goal)
  radius = (size - stroke_width) / 2
  circumference = 2 * math.pi * radius
  offset = circumference * (1 - ratio)
  center = size / 2
  font_size = max(9, round(size * 0.32))
  return (
      f"<svg width='{size}' height='{size}' viewBox='0 0 {size} {size}'"
      f" style='display:block;'>"
      f"<circle cx='{center}' cy='{center}' r='{radius}' fill='none'"
      f" stroke='#e9e9e9' stroke-width='{stroke_width}' />"
      f"<circle cx='{center}' cy='{center}' r='{radius}' fill='none'"
      f" stroke='{color}' stroke-width='{stroke_width}'"
      f" stroke-linecap='round'"
      f" stroke-dasharray='{circumference:.2f}'"
      f" stroke-dashoffset='{offset:.2f}'"
      f" transform='rotate(-90 {center} {center})' />"
      f"<text x='{center}' y='{center + font_size * 0.36:.1f}'"
      f" text-anchor='middle' font-size='{font_size}' font-weight='700'"
      f" fill='#333'>{int(minutes)}</text>"
      f"</svg>"
  )


def render_icon_box(
    icon_html, minutes, goal, box_height=88, icon_font_size=20, ring_size=42,
    click_key=None, kat_name=None, label_font_size=12,
):
  """Rendert eines der 6 Status-Kästchen (Woche/Heute) mit Icon, der
  Kategorie-Beschriftung (gleiche Optik wie im Übungsarsenal) und einem
  Fortschrittsring (samt Minutenzahl) darunter. Feste Höhe/Breite, damit
  alle 6 Boxen garantiert gleich groß sind. Wenn click_key gesetzt ist,
  erscheint darunter ein kleiner Button, der die Detailliste dieser
  Kategorie (click_key = (scope, kategorie)) öffnet."""
  ring_svg = render_progress_ring_svg(minutes, goal, size=ring_size)
  label_html = (
      f"<span class='icon-box-label' style='font-size: {label_font_size}px;"
      f" font-weight: 800; color: #1f4a34; letter-spacing: 0.2px;"
      f" line-height: 1.15;'>{kat_name}</span>"
      if kat_name
      else ""
  )
  st.markdown(
      f"<div class='icon-box' style='text-align: center; background: white;"
      f" padding: 6px; border-radius: 8px 8px 0 0; border: 1px solid"
      f" #d0edd2; border-bottom: none; width: 100%; height: {box_height}px;"
      f" box-sizing: border-box; display: flex; flex-direction: column;"
      f" align-items: center; justify-content: center; gap: 3px;"
      f" overflow: hidden;'>"
      f"<span class='icon-box-symbol' style='font-size: {icon_font_size}px;"
      f" line-height: 1;'>{icon_html}</span>"
      f"{label_html}"
      f"{ring_svg}"
      f"</div>",
      unsafe_allow_html=True,
  )
  if click_key is not None:
    scope, kat_name = click_key
    ist_aktiv = st.session_state.get("detail_ansicht") == click_key
    if st.button(
        "✕" if ist_aktiv else "🔍",
        key=f"detailbtn_{scope}_{kat_name}",
        use_container_width=True,
    ):
      st.session_state["detail_ansicht"] = None if ist_aktiv else click_key
      st.rerun()


def render_arsenal_tile(icon_html, kat_name, anzahl, box_height=82):
  """Klickbare Kategorie-Kachel fürs Übungsarsenal - gleiche Optik/Logik
  wie die Kacheln oben im Tagebuch, damit es einheitlich aussieht."""
  st.markdown(
      f"<div class='icon-box' style='text-align:center; background:white;"
      f" padding:6px; border-radius:8px 8px 0 0; border:1px solid #d0edd2;"
      f" border-bottom:none; width:100%; height:{box_height}px;"
      f" box-sizing:border-box; display:flex; flex-direction:column;"
      f" align-items:center; justify-content:center; gap:2px;'>"
      f"<span style='font-size:20px; line-height:1;'>{icon_html}</span>"
      f"<span style='font-size:12px; font-weight:800; color:#1f4a34;"
      f" letter-spacing:0.2px; line-height:1.15;'>{kat_name}</span>"
      f"<span style='font-size:11px; color:#777;'>({anzahl})</span>"
      f"</div>",
      unsafe_allow_html=True,
  )
  ist_aktiv = st.session_state.get("arsenal_detail_kat") == kat_name
  if st.button(
      "✕" if ist_aktiv else "🔍",
      key=f"arsenaltile_{kat_name}",
      use_container_width=True,
  ):
    st.session_state["arsenal_detail_kat"] = None if ist_aktiv else kat_name
    st.rerun()



@st.dialog("Sonstiges – bitte kurz beschreiben")
def sonstiges_dialog(state_key):
  """Öffnet ein modales Fenster, in dem man frei Text eintragen kann,
  wenn bei einer Kategorie die Unterkategorie 'Sonstiges' gewählt wurde."""
  text_val = st.text_area(
      "Was genau hast du gemacht?",
      value=st.session_state.get(state_key, ""),
      key=f"{state_key}_input",
  )
  col_d1, col_d2 = st.columns(2)
  with col_d1:
    if st.button(
        "Übernehmen", key=f"{state_key}_ok", type="primary",
        use_container_width=True,
    ):
      st.session_state[state_key] = text_val.strip()
      st.session_state[f"{state_key}_done"] = True
      st.rerun()
  with col_d2:
    if st.button(
        "Abbrechen", key=f"{state_key}_cancel", use_container_width=True
    ):
      st.session_state[f"{state_key}_done"] = True
      st.rerun()


def handle_sonstiges_unterkategorie(selected_unterkat, cat_key):
  """Wenn 'Sonstiges' gewählt ist, öffnet dies (einmalig, bis wieder
  gewechselt wird) das Dialog-Fenster zur Texteingabe und liefert den
  eingegebenen Freitext als tatsächliche Unterkategorie zurück."""
  state_key = f"sonstiges_text_{cat_key}"
  done_key = f"{state_key}_done"

  if selected_unterkat != "Sonstiges":
    st.session_state[done_key] = False
    return selected_unterkat

  if not st.session_state.get(done_key, False):
    sonstiges_dialog(state_key)

  freitext = st.session_state.get(state_key, "").strip()
  if freitext:
    st.caption(f"📝 Sonstiges: {freitext}")
  else:
    st.caption("📝 Sonstiges (noch keine Beschreibung eingetragen)")
  return freitext if freitext else "Sonstiges"


# Initialisierung des Session State für Daten
if "protokoll" not in st.session_state:
  st.session_state.protokoll = pd.DataFrame(
      columns=[
          "Datum",
          "Kategorie",
          "Unterkategorie",
          "Minuten",
          "Status",
          "Notizen",
      ]
  )

# Unterkategorien, die nur bei "Selbstmanagement" zur Auswahl stehen
SELBSTMANAGEMENT_UNTERKATEGORIEN = [
    "Meditation",
    "Entspannung",
    "Koordination",
    "Gleichgewichtstraining",
]

# Unterkategorien, die nur bei "Ausdauer" zur Auswahl stehen
AUSDAUER_UNTERKATEGORIEN = [
    "Joggen",
    "Nordic Walking",
    "Walking",
    "Wandern",
    "Radfahren",
    "Schwimmen",
    "Treppensteigen",
    "Sonstiges",
]

# Unterkategorien, die nur bei "Beweglichkeit" zur Auswahl stehen
BEWEGLICHKEIT_UNTERKATEGORIEN = [
    "Yoga",
    "Ausgleichsübungen",
    "Faszientraining",
    "Rückenfit",
    "Massage",
    "Sonstiges",
]

# Unterkategorien, die nur bei "Kraft" zur Auswahl stehen
KRAFT_UNTERKATEGORIEN = [
    "Pilates",
    "Rückenfit",
    "Stabilisierungstraining",
    "Therabandtraining",
    "Hanteltraining",
    "Sonstiges",
]

# Tageszeiten, die nur bei "Ernährung" zur Auswahl stehen
ERNAEHRUNG_TAGESZEITEN = ["Morgens", "Mittags", "Abends"]

# Ampel-Status für Ernährung: (Anzeige-Label, gespeicherter Wert, Farbe)
ERNAEHRUNG_AMPEL = [
    ("🟢 Umgesetzt", "Umgesetzt", "#2e7d46"),
    ("🟡 Teilweise umgesetzt", "Teilweise umgesetzt", "#e3a008"),
    ("🔴 Nicht umgesetzt", "Nicht umgesetzt", "#d9534f"),
]

# Smileys für "Gesamtbefinden"
STIMMUNG_SMILEYS = [
    ("😞 Schlecht", "😞 Schlecht"),
    ("😐 Neutral", "😐 Neutral"),
    ("😊 Gut", "😊 Gut"),
]

if "arsenal" not in st.session_state:
  st.session_state.arsenal = pd.DataFrame(
      [
          {
              "Kategorie": "Beweglichkeit",
              "Typ": "Text",
              "Bereich / Übung": "Mobilisation & Dehnen",
              "Link": "https://example.com/mobilitaet",
              "Beschreibung": "Tägliche Routine für den Rücken",
              "Bild": "",
          },
          {
              "Kategorie": "Kraft",
              "Typ": "Text",
              "Bereich / Übung": "Kräftigung Rumpf",
              "Link": "https://example.com/ruecken",
              "Beschreibung": "Aufrechte Haltung, Bauchspannung halten",
              "Bild": "",
          },
      ]
  )

# Kategorien und Typen für das Übungsarsenal (gleiche 6 Kategorien wie im
# Tagebuch, plus Typ: was für eine Art von Eintrag das ist)
ARSENAL_KATEGORIEN = [
    "Ausdauer",
    "Kraft",
    "Beweglichkeit",
    "Selbstmanagement",
    "Ernährung",
    "Gesamtbefinden",
]
ARSENAL_TYPEN = ["Bild", "Link", "Text", "Video"]

if "wochen_ansicht_aktiv" not in st.session_state:
  st.session_state.wochen_ansicht_aktiv = False

# Vitaldaten: Schritte & Gewicht (manuell oder per CSV-Import von
# Garmin/Google Fit erfasst)
if "vitaldaten" not in st.session_state:
  st.session_state.vitaldaten = pd.DataFrame(
      columns=["Datum", "Schritte", "Gewicht", "VO2max"]
  )
if "vital_form_aktiv" not in st.session_state:
  st.session_state.vital_form_aktiv = False
if "vital_import_aktiv" not in st.session_state:
  st.session_state.vital_import_aktiv = False

# ----------------------------------------------------
# 1. STARTSEITE & TAGEBUCH
# ----------------------------------------------------
if True:
  st.title("Tagebuch")
  st.markdown("##### Aktivitätentagebuch Prävention")
  st.write("---")

  # --- Automatische Datums- und Wochenberechnung ---
  heute = datetime.date.today()

  if "wochen_offset" not in st.session_state:
    st.session_state.wochen_offset = 0

  referenz_datum = heute + datetime.timedelta(
      weeks=st.session_state.wochen_offset
  )
  jahr, kalenderwoche, wochentag = referenz_datum.isocalendar()

  start_der_woche = referenz_datum - datetime.timedelta(days=wochentag - 1)
  ende_der_woche = start_der_woche + datetime.timedelta(days=6)

  monate = [
      "Jan",
      "Feb",
      "Mär",
      "Apr",
      "Mai",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Okt",
      "Nov",
      "Dez",
  ]
  start_monat = monate[start_der_woche.month - 1]
  ende_monat = monate[ende_der_woche.month - 1]

  if start_der_woche.month == ende_der_woche.month:
    datum_string = (
        f"{start_der_woche.day}. - {ende_der_woche.day}. {ende_monat}"
        f" {ende_der_woche.year}"
    )
  else:
    datum_string = (
        f"{start_der_woche.day}. {start_monat} - {ende_der_woche.day}."
        f" {ende_monat} {ende_der_woche.year}"
    )

  wochentage_de = [
      "Montag",
      "Dienstag",
      "Mittwoch",
      "Donnerstag",
      "Freitag",
      "Samstag",
      "Sonntag",
  ]
  heute_string = f"{wochentage_de[heute.weekday()]}, {heute.day}. {monate[heute.month - 1]} {heute.year}"

  df = st.session_state.protokoll

  def get_cat_minutes(kat_name):
    if df.empty or kat_name not in df["Kategorie"].values:
      return 0
    woche_df = df[
        (df["Datum"] >= str(start_der_woche))
        & (df["Datum"] <= str(ende_der_woche))
        & (df["Kategorie"] == kat_name)
    ]
    return int(woche_df["Minuten"].sum())

  def get_today_minutes(kat_name):
    if df.empty:
      return 0
    heute_str = str(heute)
    heute_df = df[(df["Datum"] == heute_str) & (df["Kategorie"] == kat_name)]
    if heute_df.empty:
      return 0
    return int(heute_df["Minuten"].sum())

  # --- CSS für den grünen Hauptkasten ---
  # Wichtig: st.container(key="dashcard") erzeugt eine echte Wrapper-Div
  # mit der CSS-Klasse "st-key-dashcard". Damit landet WIRKLICH jedes
  # Element (auch der Button "Eintrag erstellen"), das innerhalb von
  # "with st.container(key='dashcard'):" steht, in diesem Kasten -
  # der alte :has()-Marker-Trick hat das nicht zuverlässig geschafft.
  # Voraussetzung: Streamlit-Version, die den key-Parameter für
  # st.container() unterstützt (ab ca. 1.32).
  st.markdown(
      """
        <style>
        div.st-key-dashcard {
            background-color: #e2efe3;
            border: 1px solid #c8dbc9;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 25px;
        }

        /* Gleiche Kartenoptik wie beim Tagebuch, für das Übungsarsenal */
        div.st-key-arsenalcard {
            background-color: #e2efe3;
            border: 1px solid #c8dbc9;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 25px;
        }

        /* Gleiche Kartenoptik für die Vitalwerte-Karte (Schritte/Gewicht/BMI) */
        div.st-key-vitalcard {
            background-color: #e2efe3;
            border: 1px solid #c8dbc9;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 25px;
        }

        /* Primärer Aktions-Button (z.B. "Eintrag erstellen", "Speichern") -
           gefülltes, gedecktes Waldgrün, harmoniert mit der grünen Karte */
        div.stButton button[kind="primary"] {
            background-color: #3f7a5c !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            border: none !important;
        }
        div.stButton button[kind="primary"]:hover {
            background-color: #2f5e45 !important;
        }

        /* Sekundäre Buttons (Navigation ⬅️➡️, Wochen-Titel, Abbrechen) -
           dezent, outline, fügt sich ruhig in die grüne Karte ein */
        div.stButton button[kind="secondary"] {
            background-color: #ffffff !important;
            color: #2f5e45 !important;
            border: 1px solid #a9c9b3 !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }
        div.stButton button[kind="secondary"]:hover {
            background-color: #eef6f0 !important;
            border-color: #3f7a5c !important;
            color: #2f5e45 !important;
        }

        /* Spalten (st.columns) sollen auf dem Handy NICHT untereinander
           stehen, sondern genauso nebeneinander bleiben wie am Desktop.
           Streamlit stapelt Spalten normalerweise unter ~640px Breite -
           das erzwingen wir hier zurück auf eine Reihe. Wichtig: die
           prozentuale Breite (flex-basis) von Streamlit NICHT anfassen,
           sonst richten sich die Boxen nach ihrem Inhalt statt nach der
           Bildschirmbreite und werden zu breit. */
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important;
            flex-direction: row !important;
            gap: 4px !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            min-width: 0 !important;
        }

        /* Auf schmalen Handy-Screens (z.B. Poco F5, ~390-400px breit):
           Kästchen-Innenabstand, Ring-Icon und Schrift verkleinern, damit
           alle 6 Boxen pro Reihe bequem nebeneinander passen. */
        @media (max-width: 480px) {
            div.st-key-dashcard {
                padding: 8px;
            }
            div.st-key-dashcard [data-testid="stHorizontalBlock"] {
                gap: 3px !important;
            }
            .icon-box {
                padding: 3px !important;
            }
            .icon-box svg {
                width: 30px !important;
                height: 30px !important;
            }
            .icon-box .icon-box-symbol {
                font-size: 15px !important;
            }
            .icon-box .icon-box-label {
                font-size: 9px !important;
            }
        }

        /* Plus/Minus-Stepper-Buttons beim Minuten-Eingabefeld ausblenden */
        button[data-testid="stNumberInputStepDown"],
        button[data-testid="stNumberInputStepUp"] {
            display: none !important;
        }
        </style>
        """,
      unsafe_allow_html=True,
  )

  # Echter Container - alles, was hier drin (eingerückt) steht,
  # bekommt den grünen Hintergrund, inklusive des Buttons ganz unten.
  with st.container(key="dashcard"):
    col_w1, col_w2, col_w3 = st.columns([1, 4, 1])
    with col_w1:
      if st.button("⬅️", key="w_back", use_container_width=True):
        st.session_state.wochen_offset -= 1
        st.rerun()
    with col_w2:
      wochen_titel_text = (
          f"Woche {kalenderwoche} (Details ausblenden)"
          if st.session_state.wochen_ansicht_aktiv
          else f"Woche {kalenderwoche} (Details anzeigen)"
      )
      if st.button(wochen_titel_text, key="w_title", use_container_width=True):
        st.session_state.wochen_ansicht_aktiv = (
            not st.session_state.wochen_ansicht_aktiv
        )
        st.rerun()
      st.markdown(
          f"<p style='text-align: center; color: #555; margin: 0;'>{datum_string}</p>",
          unsafe_allow_html=True,
      )
    with col_w3:
      # Vorwärts-Navigation bis Ende des Jahres 2040 begrenzen
      naechste_woche_ende = ende_der_woche + datetime.timedelta(weeks=1)
      if naechste_woche_ende.year > 2040:
        st.button(
            "➡️", key="w_fwd", use_container_width=True, disabled=True
        )
      elif st.button("➡️", key="w_fwd", use_container_width=True):
        st.session_state.wochen_offset += 1
        st.rerun()

    # BEREICH: WOCHE
    st.markdown(
        "<p style='font-weight: bold; margin-top: 15px;'>Woche</p>",
        unsafe_allow_html=True,
    )
    mini_col1, mini_col2, mini_col3, mini_col4, mini_col5, mini_col6 = (
        st.columns(6)
    )
    with mini_col1:
      render_icon_box(
          "🏃‍♂️", get_cat_minutes("Ausdauer"), 90,
          box_height=108, icon_font_size=20, ring_size=44,
          click_key=("woche", "Ausdauer"), kat_name="Ausdauer",
      )
    with mini_col2:
      render_icon_box(
          "🏋️‍♂️", get_cat_minutes("Kraft"), 90,
          box_height=108, icon_font_size=20, ring_size=44,
          click_key=("woche", "Kraft"), kat_name="Kraft",
      )
    with mini_col3:
      render_icon_box(
          beweglichkeit_icon_html(30),
          get_cat_minutes("Beweglichkeit"), 90,
          box_height=108, icon_font_size=20, ring_size=44,
          click_key=("woche", "Beweglichkeit"), kat_name="Beweglichkeit",
      )
    with mini_col4:
      render_icon_box(
          "📋", get_cat_minutes("Selbstmanagement"), 90,
          box_height=108, icon_font_size=20, ring_size=44,
          click_key=("woche", "Selbstmanagement"), kat_name="Selbstmanagement",
      )
    with mini_col5:
      render_icon_box(
          "🍽️", get_cat_minutes("Ernährung"), 90,
          box_height=108, icon_font_size=20, ring_size=44,
          click_key=("woche", "Ernährung"), kat_name="Ernährung",
      )
    with mini_col6:
      render_icon_box(
          "😊", get_cat_minutes("Gesamtbefinden"), 90,
          box_height=108, icon_font_size=20, ring_size=44,
          click_key=("woche", "Gesamtbefinden"), kat_name="Gesamtbefinden",
      )

    st.write("")

    # BEREICH: HEUTE
    st.markdown(
        f"<p style='font-weight: bold;'>Heute <span style='font-size: 13px;"
        f" color: #555; float: right;'>{heute_string}</span></p>",
        unsafe_allow_html=True,
    )
    t_col1, t_col2, t_col3, t_col4, t_col5, t_col6 = st.columns(6)
    with t_col1:
      render_icon_box(
          "🏃‍♂️", get_today_minutes("Ausdauer"), 90,
          box_height=98, icon_font_size=18, ring_size=38,
          click_key=("heute", "Ausdauer"), kat_name="Ausdauer",
          label_font_size=11,
      )
    with t_col2:
      render_icon_box(
          "🏋️‍♂️", get_today_minutes("Kraft"), 90,
          box_height=98, icon_font_size=18, ring_size=38,
          click_key=("heute", "Kraft"), kat_name="Kraft",
          label_font_size=11,
      )
    with t_col3:
      render_icon_box(
          beweglichkeit_icon_html(26),
          get_today_minutes("Beweglichkeit"), 90,
          box_height=98, icon_font_size=18, ring_size=38,
          click_key=("heute", "Beweglichkeit"), kat_name="Beweglichkeit",
          label_font_size=11,
      )
    with t_col4:
      render_icon_box(
          "📋", get_today_minutes("Selbstmanagement"), 90,
          box_height=98, icon_font_size=18, ring_size=38,
          click_key=("heute", "Selbstmanagement"), kat_name="Selbstmanagement",
          label_font_size=11,
      )
    with t_col5:
      render_icon_box(
          "🍽️", get_today_minutes("Ernährung"), 90,
          box_height=98, icon_font_size=18, ring_size=38,
          click_key=("heute", "Ernährung"), kat_name="Ernährung",
          label_font_size=11,
      )
    with t_col6:
      render_icon_box(
          "😊", get_today_minutes("Gesamtbefinden"), 90,
          box_height=98, icon_font_size=18, ring_size=38,
          click_key=("heute", "Gesamtbefinden"), kat_name="Gesamtbefinden",
          label_font_size=11,
      )

    # Detail-Liste, wenn eine Kachel (Woche oder Heute) angeklickt wurde
    if st.session_state.get("detail_ansicht") is not None:
      detail_scope, detail_kat = st.session_state["detail_ansicht"]
      if detail_scope == "woche":
        detail_df = df[
            (df["Datum"] >= str(start_der_woche))
            & (df["Datum"] <= str(ende_der_woche))
            & (df["Kategorie"] == detail_kat)
        ]
        zeitraum_text = f"Woche {kalenderwoche} ({datum_string})"
      else:
        detail_df = df[
            (df["Datum"] == str(heute)) & (df["Kategorie"] == detail_kat)
        ]
        zeitraum_text = "Heute"

      st.write("---")
      st.markdown(f"#### {detail_kat} – {zeitraum_text}")
      if detail_df.empty:
        st.info(f"Noch keine Einträge für {detail_kat} in diesem Zeitraum.")
      else:
        anzeige_spalten = [
            c
            for c in [
                "Datum", "Unterkategorie", "Minuten", "Status", "Notizen"
            ]
            if c in detail_df.columns
        ]
        st.dataframe(
            detail_df[anzeige_spalten].sort_values("Datum"),
            use_container_width=True,
            hide_index=True,
        )
      if st.button("✕ Schließen", key="detail_schliessen_btn"):
        st.session_state["detail_ansicht"] = None
        st.rerun()

    st.write("")

    # Grüner Button "Eintrag erstellen" - jetzt garantiert INNERHALB
    # des grünen Kastens, da er im selben st.container(key="dashcard") steht.
    # Statt dem bunten ➕-Emoji (auf dunklem Grund schlecht erkennbar) wird
    # ein normales "+"-Zeichen verwendet, das die weiße Button-Schriftfarbe
    # übernimmt und damit gut sichtbar ist.
    if st.button(
        "＋ Eintrag erstellen",
        key="btn_create",
        use_container_width=True,
        type="primary",
    ):
      st.session_state.eintrag_modal_aktiv = True
      st.rerun()

  # Formular für Eintrag (außerhalb des Kastens)
  if st.session_state.get("eintrag_modal_aktiv", False):
    st.write("### 📝 Neuen Eintrag erfassen")
    # Kein st.form() hier: Felder innerhalb eines Formulars lösen erst
    # beim Absenden einen Rerun aus, daher würden die Zusatzfelder nicht
    # sofort erscheinen. Stattdessen normale Widgets + eigene Buttons.
    selected_cat = st.selectbox(
        "Kategorie wählen",
        [
            "Ausdauer",
            "Kraft",
            "Beweglichkeit",
            "Selbstmanagement",
            "Ernährung",
            "Gesamtbefinden",
        ],
        key="entry_kategorie",
    )

    selected_unterkat = ""
    status_wert = "Aktiv"
    minuten = 0

    if selected_cat == "Ausdauer":
      selected_unterkat = st.selectbox(
          "Unterkategorie",
          AUSDAUER_UNTERKATEGORIEN,
          key="entry_unterkategorie_ausdauer",
      )
      selected_unterkat = handle_sonstiges_unterkategorie(
          selected_unterkat, "ausdauer"
      )
      minuten = st.number_input(
          "Minuten", min_value=0, max_value=300, value=None, key="entry_minuten"
      )

    elif selected_cat == "Selbstmanagement":
      selected_unterkat = st.selectbox(
          "Unterkategorie",
          SELBSTMANAGEMENT_UNTERKATEGORIEN,
          key="entry_unterkategorie",
      )
      minuten = st.number_input(
          "Minuten", min_value=0, max_value=300, value=None, key="entry_minuten"
      )

    elif selected_cat == "Beweglichkeit":
      selected_unterkat = st.selectbox(
          "Unterkategorie",
          BEWEGLICHKEIT_UNTERKATEGORIEN,
          key="entry_unterkategorie_beweglichkeit",
      )
      selected_unterkat = handle_sonstiges_unterkategorie(
          selected_unterkat, "beweglichkeit"
      )
      minuten = st.number_input(
          "Minuten", min_value=0, max_value=300, value=None, key="entry_minuten"
      )

    elif selected_cat == "Kraft":
      selected_unterkat = st.selectbox(
          "Unterkategorie",
          KRAFT_UNTERKATEGORIEN,
          key="entry_unterkategorie_kraft",
      )
      selected_unterkat = handle_sonstiges_unterkategorie(
          selected_unterkat, "kraft"
      )
      minuten = st.number_input(
          "Minuten", min_value=0, max_value=300, value=None, key="entry_minuten"
      )

    elif selected_cat == "Ernährung":
      selected_unterkat = st.radio(
          "Tageszeit",
          ERNAEHRUNG_TAGESZEITEN,
          horizontal=True,
          key="entry_tageszeit",
      )
      ampel_label = st.radio(
          "Status",
          [label for label, _, _ in ERNAEHRUNG_AMPEL],
          horizontal=True,
          key="entry_ampel",
      )
      status_wert = next(
          wert for label, wert, _ in ERNAEHRUNG_AMPEL if label == ampel_label
      )

    elif selected_cat == "Gesamtbefinden":
      smiley_label = st.radio(
          "Stimmung wählen",
          [label for label, _ in STIMMUNG_SMILEYS],
          horizontal=True,
          key="entry_smiley",
      )
      selected_unterkat = next(
          wert for label, wert in STIMMUNG_SMILEYS if label == smiley_label
      )

    else:
      minuten = st.number_input(
          "Minuten", min_value=0, max_value=300, value=None, key="entry_minuten"
      )

    datum = st.date_input("Datum", value=heute, key="entry_datum")
    notizen = st.text_input("Notizen / Details", key="entry_notizen")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
      save_btn = st.button(
          "Speichern",
          key="save_entry_btn",
          type="primary",
          use_container_width=True,
      )
    with col_s2:
      cancel_btn = st.button(
          "Abbrechen", key="cancel_entry_btn", use_container_width=True
      )

    if save_btn:
      neuer_eintrag = pd.DataFrame(
          [{
              "Datum": str(datum),
              "Kategorie": selected_cat,
              "Unterkategorie": selected_unterkat,
              "Minuten": minuten if minuten is not None else 0,
              "Status": status_wert,
              "Notizen": notizen,
          }]
      )
      st.session_state.protokoll = pd.concat(
          [st.session_state.protokoll, neuer_eintrag], ignore_index=True
      )
      st.session_state.eintrag_modal_aktiv = False
      st.success("Eintrag erfolgreich gespeichert!")
      st.rerun()
    if cancel_btn:
      st.session_state.eintrag_modal_aktiv = False
      st.rerun()
    st.write("---")


  # WOCHEN-ANSICHT (3x2 Raster wenn aktiviert)
  if st.session_state.wochen_ansicht_aktiv:
    st.write("### 📊 Detail-Auswertung der Kategorien (3x2)")

    def get_cat_stats(kat_name):
      woche_df_all = df[
          (df["Datum"] >= str(start_der_woche))
          & (df["Datum"] <= str(ende_der_woche))
      ]
      if woche_df_all.empty or kat_name not in woche_df_all["Kategorie"].values:
        return 0, "Noch keine Einträge", "⚪"
      kat_df = woche_df_all[woche_df_all["Kategorie"] == kat_name]
      min_sum = kat_df["Minuten"].sum()
      if min_sum >= 90:
        return min_sum, f"{min_sum} min (Ausreichend)", "🟢"
      elif min_sum >= 60:
        return min_sum, f"{min_sum} min (Mittel)", "🟡"
      else:
        return (
            min_sum,
            (
                f"{min_sum} min (Zu wenig)"
                if min_sum > 0
                else "Noch keine Einträge"
            ),
            "🔴" if min_sum > 0 else "⚪",
        )

    kategorien_paare = [
        (("🏃‍♂️ Ausdauer", "Ausdauer"), ("🏋️‍♂️ Kraft", "Kraft")),
        (
            (f"{beweglichkeit_icon_html(20)} Beweglichkeit", "Beweglichkeit"),
            ("📋 Selbstmanagement", "Selbstmanagement"),
        ),
        (("🍽️ Ernährung", "Ernährung"), ("😊 Gesamtbefinden", "Gesamtbefinden")),
    ]

    for kat1, kat2 in kategorien_paare:
      c1, c2 = st.columns(2)
      m1, text1, sym1 = get_cat_stats(kat1[1])
      with c1:
        st.markdown(
            f"""
                    <div style="padding: 15px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 10px; background-color: #f9f9f9; height: 90px;">
                        <h4 style="margin: 0; color: #333; font-size: 16px;">{kat1[0]}</h4>
                        <p style="margin: 8px 0 0 0; font-size: 14px; color: #555;">{sym1} {text1}</p>
                    </div>
                    """,
            unsafe_allow_html=True,
        )

      m2, text2, sym2 = get_cat_stats(kat2[1])
      with c2:
        st.markdown(
            f"""
                    <div style="padding: 15px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 10px; background-color: #f9f9f9; height: 90px;">
                        <h4 style="margin: 0; color: #333; font-size: 16px;">{kat2[0]}</h4>
                        <p style="margin: 8px 0 0 0; font-size: 14px; color: #555;">{sym2} {text2}</p>
                    </div>
                    """,
            unsafe_allow_html=True,
        )

    gesamt_minuten = (
        df[
            (df["Datum"] >= str(start_der_woche))
            & (df["Datum"] <= str(ende_der_woche))
        ]["Minuten"].sum()
        if not df.empty
        else 0
    )
    if gesamt_minuten >= 90:
      g_sym, g_text = "🟢", f"{gesamt_minuten} min — Ausreichend (Ziel erreicht)"
    elif gesamt_minuten >= 60:
      g_sym, g_text = "🟡", f"{gesamt_minuten} min — Mittel"
    else:
      g_sym, g_text = (
          ("🔴", f"{gesamt_minuten} min — Zu wenig")
          if gesamt_minuten > 0
          else ("⚪", "Noch keine Einträge")
      )

    st.markdown(
        f"""
        <div style="padding: 18px; border: 2px solid #2F4F4F; border-radius: 10px; margin-top: 10px; margin-bottom: 20px; background-color: #E0EEEE;">
            <h3 style="margin: 0; color: #2F4F4F; font-size: 18px;">📊 Gesamtauswertung dieser Woche</h3>
            <p style="margin: 8px 0 0 0; font-size: 15px; font-weight: bold; color: #333;">{g_sym} {g_text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("---")

  # ----------------------------------------------------
  # VITALWERTE: Schritte, Gewicht, BMI
  # ----------------------------------------------------
  vital_df = st.session_state.vitaldaten

  def _vital_heute(spalte):
    if vital_df.empty:
      return None
    treffer = vital_df[vital_df["Datum"] == str(heute)]
    if treffer.empty or treffer[spalte].dropna().empty:
      return None
    return treffer[spalte].dropna().iloc[-1]

  def _vital_woche_avg(spalte):
    if vital_df.empty:
      return None
    woche_df = vital_df[
        (vital_df["Datum"] >= str(start_der_woche))
        & (vital_df["Datum"] <= str(ende_der_woche))
    ]
    werte = woche_df[spalte].dropna()
    if werte.empty:
      return None
    return werte.mean()

  def _vital_letzter_wert(spalte):
    """Letzter bekannter (nicht-leerer) Wert insgesamt - für Werte wie
    VO2max, die sich nicht täglich ändern, sondern nur gelegentlich neu
    gemessen/geschätzt werden."""
    if vital_df.empty or spalte not in vital_df.columns:
      return None
    sortiert = vital_df.sort_values("Datum")
    werte = sortiert[spalte].dropna()
    if werte.empty:
      return None
    return werte.iloc[-1]

  schritte_heute = _vital_heute("Schritte")
  schritte_woche_avg = _vital_woche_avg("Schritte")
  gewicht_heute = _vital_heute("Gewicht")
  gewicht_woche_avg = _vital_woche_avg("Gewicht")
  vo2max_aktuell = _vital_letzter_wert("VO2max")

  if "koerpergroesse_cm" not in st.session_state:
    st.session_state.koerpergroesse_cm = None

  bmi_wert = None
  if gewicht_heute and st.session_state.koerpergroesse_cm:
    groesse_m = st.session_state.koerpergroesse_cm / 100
    bmi_wert = gewicht_heute / (groesse_m**2)

  with st.container(key="vitalcard"):
    st.subheader("📊 Vitalwerte")

    groesse_input = st.number_input(
        "Körpergröße (cm) – einmalig für BMI-Berechnung",
        min_value=0,
        max_value=250,
        value=st.session_state.koerpergroesse_cm,
        key="groesse_input",
    )
    st.session_state.koerpergroesse_cm = (
        groesse_input if groesse_input else None
    )

    m_col1, m_col2, m_col3, m_col4, m_col5, m_col6 = st.columns(6)
    with m_col1:
      st.metric(
          "Schritte heute",
          f"{int(schritte_heute):,}".replace(",", ".")
          if schritte_heute is not None
          else "–",
      )
    with m_col2:
      st.metric(
          "Ø Schritte/Tag (Woche)",
          f"{int(schritte_woche_avg):,}".replace(",", ".")
          if schritte_woche_avg is not None
          else "–",
      )
    with m_col3:
      st.metric(
          "Gewicht heute",
          f"{gewicht_heute:.1f} kg" if gewicht_heute is not None else "–",
      )
    with m_col4:
      st.metric(
          "Ø Gewicht (Woche)",
          f"{gewicht_woche_avg:.1f} kg"
          if gewicht_woche_avg is not None
          else "–",
      )
    with m_col5:
      st.metric(
          "BMI", f"{bmi_wert:.1f}" if bmi_wert is not None else "–"
      )
    with m_col6:
      st.metric(
          "VO2max (aktuell)",
          f"{vo2max_aktuell:.1f}" if vo2max_aktuell is not None else "–",
      )

    st.write("")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
      if st.button(
          "＋ Schritte/Gewicht eintragen",
          key="btn_open_vital_form",
          type="primary",
          use_container_width=True,
      ):
        st.session_state.vital_form_aktiv = True
        st.session_state.vital_import_aktiv = False
        st.rerun()
    with col_v2:
      if st.button(
          "⬆️ CSV importieren",
          key="btn_open_vital_import",
          use_container_width=True,
      ):
        st.session_state.vital_import_aktiv = True
        st.session_state.vital_form_aktiv = False
        st.rerun()

    if st.session_state.vital_form_aktiv:
      st.write("---")
      v_datum = st.date_input("Datum", value=heute, key="vital_datum")
      v_schritte = st.number_input(
          "Schritte", min_value=0, max_value=100000, value=None,
          key="vital_schritte_input",
      )
      v_gewicht = st.number_input(
          "Gewicht (kg)", min_value=0.0, max_value=400.0, value=None,
          step=0.1, key="vital_gewicht_input",
      )
      v_vo2max = st.number_input(
          "VO2max (ml/kg/min) – optional, meist von der Uhr geschätzt",
          min_value=0.0, max_value=100.0, value=None,
          step=0.1, key="vital_vo2max_input",
      )
      col_vs1, col_vs2 = st.columns(2)
      with col_vs1:
        vital_save = st.button(
            "Speichern", key="vital_save_btn", type="primary",
            use_container_width=True,
        )
      with col_vs2:
        vital_cancel = st.button(
            "Abbrechen", key="vital_cancel_btn", use_container_width=True
        )
      if vital_save:
        neuer_vital_eintrag = pd.DataFrame(
            [{
                "Datum": str(v_datum),
                "Schritte": v_schritte,
                "Gewicht": v_gewicht,
                "VO2max": v_vo2max,
            }]
        )
        st.session_state.vitaldaten = pd.concat(
            [st.session_state.vitaldaten, neuer_vital_eintrag],
            ignore_index=True,
        )
        st.session_state.vital_form_aktiv = False
        st.success("Gespeichert!")
        st.rerun()
      if vital_cancel:
        st.session_state.vital_form_aktiv = False
        st.rerun()

    if st.session_state.vital_import_aktiv:
      st.write("---")
      st.caption(
          "Exportiere deine Daten bei Garmin Connect (Einstellungen ›"
          " Daten exportieren) oder bei Google Fit / Health Connect (über"
          " Google Takeout) als CSV und lade die Datei hier hoch."
      )
      csv_upload = st.file_uploader(
          "CSV-Datei auswählen", type=["csv"], key="vital_csv_upload"
      )
      if csv_upload is not None:
        try:
          import_df = pd.read_csv(csv_upload)
          st.write("Vorschau:")
          st.dataframe(import_df.head(), use_container_width=True)

          spalten = import_df.columns.tolist()
          keine_option = "– keine –"
          datum_spalte = st.selectbox(
              "Welche Spalte enthält das Datum?",
              spalten,
              key="csv_datum_spalte",
          )
          schritte_spalte = st.selectbox(
              "Welche Spalte enthält die Schritte? (optional)",
              [keine_option] + spalten,
              key="csv_schritte_spalte",
          )
          gewicht_spalte = st.selectbox(
              "Welche Spalte enthält das Gewicht in kg? (optional)",
              [keine_option] + spalten,
              key="csv_gewicht_spalte",
          )
          vo2max_spalte = st.selectbox(
              "Welche Spalte enthält VO2max? (optional)",
              [keine_option] + spalten,
              key="csv_vo2max_spalte",
          )

          if st.button(
              "Importieren", key="csv_import_btn", type="primary"
          ):
            neue_zeilen = pd.DataFrame()
            neue_zeilen["Datum"] = pd.to_datetime(
                import_df[datum_spalte], errors="coerce"
            ).dt.strftime("%Y-%m-%d")
            neue_zeilen["Schritte"] = (
                pd.to_numeric(
                    import_df[schritte_spalte], errors="coerce"
                )
                if schritte_spalte != keine_option
                else None
            )
            neue_zeilen["Gewicht"] = (
                pd.to_numeric(
                    import_df[gewicht_spalte], errors="coerce"
                )
                if gewicht_spalte != keine_option
                else None
            )
            neue_zeilen["VO2max"] = (
                pd.to_numeric(
                    import_df[vo2max_spalte], errors="coerce"
                )
                if vo2max_spalte != keine_option
                else None
            )
            neue_zeilen = neue_zeilen.dropna(subset=["Datum"])
            st.session_state.vitaldaten = pd.concat(
                [st.session_state.vitaldaten, neue_zeilen],
                ignore_index=True,
            )
            st.session_state.vital_import_aktiv = False
            st.success(f"{len(neue_zeilen)} Zeilen importiert!")
            st.rerun()
        except Exception as e:
          st.error(f"CSV konnte nicht gelesen werden: {e}")

      if st.button("Abbrechen", key="vital_import_cancel_btn"):
        st.session_state.vital_import_aktiv = False
        st.rerun()

  st.write("### Bisherige Protokoll-Einträge")
  if not df.empty:
    st.dataframe(df, use_container_width=True)

    @st.cache_data
    def convert_df_to_excel(dataframe):
      from io import BytesIO

      output = BytesIO()
      with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="Protokoll")
      return output.getvalue()

    excel_data = convert_df_to_excel(df)
    st.download_button(
        label="📥 Als Excel-Datei herunterladen",
        data=excel_data,
        file_name="Sport_Tagebuch.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
  else:
    st.info("Noch keine Einträge vorhanden.")

# ----------------------------------------------------
# 2. ÜBUNGSARSENAL (direkt unter dem Tagebuch, keine eigene Seite mehr)
# ----------------------------------------------------
if True:
  st.write("---")
  st.title("🏋️‍♀️ Übungsarsenal")
  st.write("Deine Sammlung von Links, Bereichen und Übungs-Hinweisen.")

  with st.container(key="arsenalcard"):
    if st.session_state.arsenal.empty:
      st.info("Noch keine Einträge im Übungsarsenal.")
    else:
      arsenal_df = st.session_state.arsenal
      arsenal_icons = {
          "Ausdauer": "🏃‍♂️",
          "Kraft": "🏋️‍♂️",
          "Beweglichkeit": beweglichkeit_icon_html(22),
          "Selbstmanagement": "📋",
          "Ernährung": "🍽️",
          "Gesamtbefinden": "😊",
      }

      a_col1, a_col2, a_col3, a_col4, a_col5, a_col6 = st.columns(6)
      for spalte, kat in zip(
          [a_col1, a_col2, a_col3, a_col4, a_col5, a_col6],
          ARSENAL_KATEGORIEN,
      ):
        with spalte:
          anzahl = len(arsenal_df[arsenal_df["Kategorie"] == kat])
          render_arsenal_tile(arsenal_icons.get(kat, "📌"), kat, anzahl)

      # Detail-Liste für die angeklickte Kategorie
      aktive_kat = st.session_state.get("arsenal_detail_kat")
      if aktive_kat is not None:
        kat_eintraege = arsenal_df[arsenal_df["Kategorie"] == aktive_kat]
        st.write("---")
        st.markdown(f"#### {aktive_kat} ({len(kat_eintraege)})")
        if kat_eintraege.empty:
          st.info(f"Noch keine Einträge für {aktive_kat}.")
        else:
          for _, eintrag in kat_eintraege.iterrows():
            with st.container(border=True):
              st.markdown(
                  f"<div style='display:flex; justify-content:space-between;"
                  f" align-items:center; flex-wrap:wrap; gap:6px;'>"
                  f"<span style='font-weight:700; font-size:16px;'>"
                  f"{eintrag.get('Bereich / Übung', '')}</span>"
                  f"<span style='background:#e2efe3; color:#2f5e45;"
                  f" padding:2px 10px; border-radius:12px; font-size:12px;"
                  f" font-weight:600; white-space:nowrap;'>"
                  f"{eintrag.get('Typ', '')}</span></div>",
                  unsafe_allow_html=True,
              )
              if eintrag.get("Beschreibung"):
                st.write(eintrag["Beschreibung"])
              if eintrag.get("Link"):
                st.markdown(f"🔗 [{eintrag['Link']}]({eintrag['Link']})")
              if eintrag.get("Bild"):
                st.image(eintrag["Bild"], use_container_width=True)
        if st.button("✕ Schließen", key="arsenal_detail_schliessen_btn"):
          st.session_state["arsenal_detail_kat"] = None
          st.rerun()

      # Falls Einträge eine Kategorie außerhalb der Standardliste haben
      # (z.B. durch ältere Daten), trotzdem anzeigen statt zu verschlucken
      sonstige = arsenal_df[~arsenal_df["Kategorie"].isin(ARSENAL_KATEGORIEN)]
      if not sonstige.empty:
        with st.expander(f"Sonstige ({len(sonstige)})"):
          for _, eintrag in sonstige.iterrows():
            with st.container(border=True):
              st.markdown(f"**{eintrag.get('Bereich / Übung', '')}**")
              if eintrag.get("Beschreibung"):
                st.write(eintrag["Beschreibung"])
              if eintrag.get("Link"):
                st.markdown(f"🔗 [{eintrag['Link']}]({eintrag['Link']})")
              if eintrag.get("Bild"):
                st.image(eintrag["Bild"], use_container_width=True)

    st.write("")
    if "arsenal_form_aktiv" not in st.session_state:
      st.session_state.arsenal_form_aktiv = False

    if not st.session_state.arsenal_form_aktiv:
      if st.button(
          "＋ Neuen Link / Eintrag hinzufügen",
          key="btn_open_arsenal_form",
          type="primary",
          use_container_width=True,
      ):
        st.session_state.arsenal_form_aktiv = True
        st.rerun()
    else:
      st.subheader("Neuen Link / Eintrag hinzufügen")
      kategorie = st.selectbox(
          "Kategorie", ARSENAL_KATEGORIEN, key="arsenal_kategorie"
      )
      titel = st.text_input(
          "Titel (z. B. \"Kräftigung Rumpfmuskulatur\")",
          key="arsenal_titel",
      )
      typ = st.selectbox("Typ", ARSENAL_TYPEN, key="arsenal_typ")
      link = st.text_input("Link / URL", key="arsenal_link")
      beschreibung = st.text_area(
          "Beschreibung / Notiz", key="arsenal_beschreibung"
      )
      bild_upload = st.file_uploader(
          "Screenshot / Bild zur Übung (optional)",
          type=["png", "jpg", "jpeg"],
          key="arsenal_bild",
      )

      col_a1, col_a2 = st.columns(2)
      with col_a1:
        arsenal_submitted = st.button(
            "Hinzufügen",
            key="arsenal_submit_btn",
            type="primary",
            use_container_width=True,
        )
      with col_a2:
        arsenal_cancelled = st.button(
            "Abbrechen",
            key="arsenal_cancel_btn",
            use_container_width=True,
        )

      if arsenal_submitted:
        bild_data_uri = ""
        if bild_upload is not None:
          bild_b64 = base64.b64encode(bild_upload.getvalue()).decode("utf-8")
          bild_data_uri = f"data:{bild_upload.type};base64,{bild_b64}"

        neuer_link = pd.DataFrame(
            [{
                "Kategorie": kategorie,
                "Typ": typ,
                "Bereich / Übung": titel,
                "Link": link,
                "Beschreibung": beschreibung,
                "Bild": bild_data_uri,
            }]
        )
        st.session_state.arsenal = pd.concat(
            [st.session_state.arsenal, neuer_link], ignore_index=True
        )
        st.session_state.arsenal_form_aktiv = False
        st.success("Erfolgreich hinzugefügt!")
        st.rerun()
      if arsenal_cancelled:
        st.session_state.arsenal_form_aktiv = False
        st.rerun()
