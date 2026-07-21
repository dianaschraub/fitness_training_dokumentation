
import datetime
import pandas as pd
import streamlit as st

# Seiten-Konfiguration
st.set_page_config(
    page_title="Sport-Tagebuch", page_icon="🏃‍♀️", layout="centered"
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


  def get_cat_symbol(kat_name):
    if df.empty or kat_name not in df["Kategorie"].values:
      return "⚪"
    min_sum = df[df["Kategorie"] == kat_name]["Minuten"].sum()
    if min_sum >= 90:
      return "🟢"
    elif min_sum >= 60:
      return "🟡"
    else:
      return "🔴" if min_sum > 0 else "⚪"


  def get_today_symbol(kat_name):
    if df.empty:
      return "⚪"
    heute_str = str(heute)
    heute_df = df[(df["Datum"] == heute_str) & (df["Kategorie"] == kat_name)]
    if heute_df.empty:
      return "⚪"
    min_sum = heute_df["Minuten"].sum()
    if min_sum >= 30:
      return "🟢"
    elif min_sum > 0:
      return "🟡"
    else:
      return "🔴"


  # --- GESAMTER GRÜNER CONTAINER (Woche bis Button) ---
  st.markdown(
      """
        <style>
        .custom-green-box {
            background-color: #e2efe3;
            border: 1px solid #c8dbc9;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .stButton button[kind="primary"] {
            background-color: #0077b6 !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            border: none !important;
        }
        .stButton button[kind="primary"]:hover {
            background-color: #023e8a !important;
        }
        </style>
        <div class="custom-green-box">
        """,
      unsafe_allow_html=True,
  )

  # Wochen-Kopfzeile
  col_w1, col_w2, col_w3 = st.columns([1, 4, 1])
  with col_w1:
    if st.button("⬅️", use_container_width=True):
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
    if st.button(wochen_titel_text, use_container_width=True):
      st.session_state.wochen_ansicht_aktiv = (
          not st.session_state.wochen_ansicht_aktiv
      )
      st.rerun()
    st.markdown(
        f"<p style='text-align: center; color: #555; margin: 0;'>{datum_string}</p>",
        unsafe_allow_html=True,
    )
  with col_w3:
    if st.button("➡️", use_container_width=True):
      st.session_state.wochen_ansicht_aktiv = (
          not st.session_state.wochen_ansicht_aktiv
      )
      st.rerun()

  # BEREICH: WOCHE
  st.markdown("<p style='font-weight: bold; margin-top: 15px;'>Woche</p>", unsafe_allow_html=True)
  mini_col1, mini_col2, mini_col3, mini_col4, mini_col5, mini_col6 = (
      st.columns(6)
  )
  with mini_col1:
    st.markdown(
        f"<div style='text-align: center; font-size: 20px; background: white; padding: 6px; border-radius: 8px; border: 1px solid #d0edd2;'>🏃‍♂️<br><span style='font-size: 16px;'>{get_cat_symbol('Ausdauer')}</span></div>",
        unsafe_allow_html=True,
    )
  with mini_col2:
    st.markdown(
        f"<div style='text-align: center; font-size: 20px; background: white; padding: 6px; border-radius: 8px; border: 1px solid #d0edd2;'>🏋️‍♂️<br><span style='font-size: 16px;'>{get_cat_symbol('Kraft')}</span></div>",
        unsafe_allow_html=True,
    )
  with mini_col3:
    st.markdown(
        f"<div style='text-align: center; font-size: 20px; background: white; padding: 6px; border-radius: 8px; border: 1px solid #d0edd2;'>🚶‍♂️<br><span style='font-size: 16px;'>{get_cat_symbol('Beweglichkeit')}</span></div>",
        unsafe_allow_html=True,
    )
  with mini_col4:
    st.markdown(
        f"<div style='text-align: center; font-size: 20px; background: white; padding: 6px; border-radius: 8px; border: 1px solid #d0edd2;'>📋<br><span style='font-size: 16px;'>{get_cat_symbol('Selbstmanagement')}</span></div>",
        unsafe_allow_html=True,
    )
  with mini_col5:
    st.markdown(
        f"<div style='text-align: center; font-size: 20px; background: white; padding: 6px; border-radius: 8px; border: 1px solid #d0edd2;'>🍽️<br><span style='font-size: 16px;'>{get_cat_symbol('Ernährung')}</span></div>",
        unsafe_allow_html=True,
    )
  with mini_col6:
    st.markdown(
        f"<div style='text-align: center; font-size: 20px; background: white; padding: 6px; border-radius: 8px; border: 1px solid #d0edd2;'>😊<br><span style='font-size: 16px;'>{get_cat_symbol('Gesamtbefinden')}</span></div>",
        unsafe_allow_html=True,
    )

  st.write("")

  # BEREICH: HEUTE
  st.markdown(
      f"<p style='font-weight: bold;'>Heute <span style='font-size: 13px; color: #555; float: right;'>{heute_string}</span></p>",
      unsafe_allow_html=True,
  )
  t_col1, t_col2, t_col3, t_col4, t_col5, t_col6 = st.columns(6)
  with t_col1:
    st.markdown(
        f"<div style='text-align: center; font-size: 18px; background: white; padding: 6px; border-radius: 8px; border: 1px solid #d0edd2;'>🏃‍♂️<br><span style='font-size: 15px;'>{get_today_symbol('Ausdauer')}</span></div>",
        unsafe_allow_html=True,
    )
  with t_col2:
    st.markdown(
        f"<div style='text-align: center; font-size: 18px; background: white; padding: 6px; border-radius: 8px; border: 1px solid #d0edd2;'>🏋️‍♂️<br><span style='font-size: 15px;'>{get_today_symbol('Kraft')}</span></div>",
        unsafe_allow_html=True,
    )
  with t_col3:
    st.markdown(
        f"<div style='text-align: center; font-size: 18px; background: white; padding: 6px; border-radius: 8px; border: 1px solid #d0edd2;'>🚶‍♂️<br><span style='font-size: 15px;'>{get_today_symbol('Beweglichkeit')}</span></div>",
        unsafe_allow_html=True,
    )
  with t_col4:
    st.markdown(
        f"<div style='text-align: center; font-size: 18px; background: white; padding: 6px; border-radius: 8px; border: 1px solid #d0edd2;'>📋<br><span style='font-size: 15px;'>{get_today_symbol('Selbstmanagement')}</span></div>",
        unsafe_allow_html=True,
    )
  with t_col5:
    st.markdown(
        f"<div style='text-align: center; font-size: 18px; background: white; padding: 6px; border-radius: 8px; border: 1px solid #d0edd2;'>🍽️<br><span style='font-size: 15px;'>{get_today_symbol('Ernährung')}</span></div>",
        unsafe_allow_html=True,
    )
  with t_col6:
    st.markdown(
        f"<div style='text-align: center; font-size: 18px; background: white; padding: 6px; border-radius: 8px; border: 1px solid #d0edd2;'>😊<br><span style='font-size: 15px;'>{get_today_symbol('Gesamtbefinden')}</span></div>",
        unsafe_allow_html=True,
    )

  st.write("")

  # BLauer Button "Eintrag erstellen" innerhalb des grünen Containers
  if st.button("➕ Eintrag erstellen", use_container_width=True, type="primary"):
    st.session_state.eintrag_modal_aktiv = True
    st.rerun()

  # Ende des grünen Containers
  st.markdown("</div>", unsafe_allow_html=True)

  # Formular für Eintrag
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
        (("🚶‍♂️ Beweglichkeit", "Beweglichkeit"), ("📋 Selbstmanagement", "Selbstmanagement")),
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

    arsenal_submitted = st.form_submit_button("Hinzufügen")
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
