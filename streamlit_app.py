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
    icon_html, minutes, goal, box_height=88, icon_font_size=20, ring_size=42
):
  """Rendert eines der 6 Status-Kästchen (Woche/Heute) mit Icon oben und
  einem Fortschrittsring (samt Minutenzahl) darunter. Feste Höhe/Breite,
  damit alle 6 Boxen garantiert gleich groß sind."""
  ring_svg = render_progress_ring_svg(minutes, goal, size=ring_size)
  st.markdown(
      f"<div style='text-align: center; background: white; padding: 6px;"
      f" border-radius: 8px; border: 1px solid #d0edd2; width: 100%;"
      f" height: {box_height}px; box-sizing: border-box; display: flex;"
      f" flex-direction: column; align-items: center; justify-content:"
      f" center; gap: 4px;'>"
      f"<span style='font-size: {icon_font_size}px; line-height: 1;'>"
      f"{icon_html}</span>"
      f"{ring_svg}"
      f"</div>",
      unsafe_allow_html=True,
  )

# Initialisierung des Session State für Daten
if "protokoll" not in st.session_state:
  st.session_state.protokoll = pd.DataFrame(
      columns=["Datum", "Kategorie", "Minuten", "Status", "Notizen"]
  )

if "arsenal" not in st.session_state:
  st.session_state.arsenal = pd.DataFrame(
      [
          {
              "Bereich / Übung": "Mobilisation & Dehnen",
              "Kategorie": "Bereich",
              "Link": "https://example.com/mobilitaet",
              "Beschreibung": "Tägliche Routine für den Rücken",
          },
          {
              "Bereich / Übung": "Kräftigung Rumpf",
              "Kategorie": "Übung",
              "Link": "https://example.com/ruecken",
              "Beschreibung": "Aufrechte Haltung, Bauchspannung halten",
          },
      ]
  )

if "wochen_ansicht_aktiv" not in st.session_state:
  st.session_state.wochen_ansicht_aktiv = False

# Navigation via Sidebar
menu = st.sidebar.selectbox(
    "Navigation",
    ["Startseite & Tagebuch", "Übungsarsenal"],
)

# ----------------------------------------------------
# 1. STARTSEITE & TAGEBUCH
# ----------------------------------------------------
if menu == "Startseite & Tagebuch":
  st.title("Tagebuch")
  st.markdown("##### Aktivitätentagebuch Prävention")
  st.write("---")

  # --- Automatische Datums- und Wochenberechnung ---
  heute = datetime.date.today()
  jahr, kalenderwoche, wochentag = heute.isocalendar()

  start_der_woche = heute - datetime.timedelta(days=wochentag - 1)
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
    return int(df[df["Kategorie"] == kat_name]["Minuten"].sum())

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
        st.session_state.wochen_ansicht_aktiv = (
            not st.session_state.wochen_ansicht_aktiv
        )
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
      if st.button("➡️", key="w_fwd", use_container_width=True):
        st.session_state.wochen_ansicht_aktiv = (
            not st.session_state.wochen_ansicht_aktiv
        )
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
          box_height=90, icon_font_size=20, ring_size=44,
      )
    with mini_col2:
      render_icon_box(
          "🏋️‍♂️", get_cat_minutes("Kraft"), 90,
          box_height=90, icon_font_size=20, ring_size=44,
      )
    with mini_col3:
      render_icon_box(
          beweglichkeit_icon_html(30),
          get_cat_minutes("Beweglichkeit"), 90,
          box_height=90, icon_font_size=20, ring_size=44,
      )
    with mini_col4:
      render_icon_box(
          "📋", get_cat_minutes("Selbstmanagement"), 90,
          box_height=90, icon_font_size=20, ring_size=44,
      )
    with mini_col5:
      render_icon_box(
          "🍽️", get_cat_minutes("Ernährung"), 90,
          box_height=90, icon_font_size=20, ring_size=44,
      )
    with mini_col6:
      render_icon_box(
          "😊", get_cat_minutes("Gesamtbefinden"), 90,
          box_height=90, icon_font_size=20, ring_size=44,
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
          box_height=80, icon_font_size=18, ring_size=38,
      )
    with t_col2:
      render_icon_box(
          "🏋️‍♂️", get_today_minutes("Kraft"), 90,
          box_height=80, icon_font_size=18, ring_size=38,
      )
    with t_col3:
      render_icon_box(
          beweglichkeit_icon_html(26),
          get_today_minutes("Beweglichkeit"), 90,
          box_height=80, icon_font_size=18, ring_size=38,
      )
    with t_col4:
      render_icon_box(
          "📋", get_today_minutes("Selbstmanagement"), 90,
          box_height=80, icon_font_size=18, ring_size=38,
      )
    with t_col5:
      render_icon_box(
          "🍽️", get_today_minutes("Ernährung"), 90,
          box_height=80, icon_font_size=18, ring_size=38,
      )
    with t_col6:
      render_icon_box(
          "😊", get_today_minutes("Gesamtbefinden"), 90,
          box_height=80, icon_font_size=18, ring_size=38,
      )

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
    with st.form(key="kategorie_form"):
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
      )
      datum = st.date_input("Datum", value=heute)
      minuten = st.number_input(
          "Minuten", min_value=0, max_value=300, value=30
      )
      notizen = st.text_input("Notizen / Details")

      col_s1, col_s2 = st.columns(2)
      with col_s1:
        save_btn = st.form_submit_button("Speichern", type="primary")
      with col_s2:
        cancel_btn = st.form_submit_button("Abbrechen")

      if save_btn:
        neuer_eintrag = pd.DataFrame(
            [{
                "Datum": str(datum),
                "Kategorie": selected_cat,
                "Minuten": minuten,
                "Status": "Aktiv",
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
      if df.empty or kat_name not in df["Kategorie"].values:
        return 0, "Noch keine Einträge", "⚪"
      kat_df = df[df["Kategorie"] == kat_name]
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

    gesamt_minuten = df["Minuten"].sum() if not df.empty else 0
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
# 2. ÜBUNGSARSENAL
# ----------------------------------------------------
elif menu == "Übungsarsenal":
  st.title("🏋️‍♀️ Übungsarsenal")
  st.write("Deine Sammlung von Links, Bereichen und Übungs-Hinweisen.")

  st.dataframe(st.session_state.arsenal, use_container_width=True)

  st.write("---")
  st.subheader("Neuen Link / Eintrag hinzufügen")
  with st.form("arsenal_form"):
    titel = st.text_input("Bereich oder Übung")
    kategorie = st.selectbox("Kategorie", ["Bereich", "Übung"])
    link = st.text_input("Link / URL")
    beschreibung = st.text_area("Beschreibung / Notiz")

    arsenal_submitted = st.form_submit_button("Hinzufügen", type="primary")
    if arsenal_submitted:
      neuer_link = pd.DataFrame(
          [{
              "Bereich / Übung": titel,
              "Kategorie": kategorie,
              "Link": link,
              "Beschreibung": beschreibung,
          }]
      )
      st.session_state.arsenal = pd.concat(
          [st.session_state.arsenal, neuer_link], ignore_index=True
      )
      st.success("Erfolgreich hinzugefügt!")
