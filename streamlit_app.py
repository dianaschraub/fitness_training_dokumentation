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

# Navigation via Sidebar
menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Startseite & Tagebuch",
        "Eintrag erstellen (Kategorien)",
        "Übungsarsenal",
    ],
)

# ----------------------------------------------------
# 1. STARTSEITE & TAGEBUCH (3x2 Raster + Gesamtauswertung)
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

  # Wochen-Kopfzeile
  col_w1, col_w2, col_w3 = st.columns([1, 4, 1])
  with col_w1:
    st.markdown("### ⬅️")
  with col_w2:
    st.markdown(
        f"<h3 style='text-align: center;'>Woche {kalenderwoche}</h3>"
        f"<p style='text-align: center; color: gray;'>{datum_string}</p>",
        unsafe_allow_html=True,
    )
  with col_w3:
    st.markdown("### ➡️")

  st.write("---")

  # Button "Eintrag erstellen"
  if st.button("➕ Eintrag erstellen", use_container_width=True, type="primary"):
    st.session_state.nav_override = "Eintrag erstellen (Kategorien)"
    st.rerun()

  st.write("### Auswertung nach Kategorien")

  df = st.session_state.protokoll


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


  # 6 Kategorien in 3 Zeilen a 2 Spalten aufteilen
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

  # Gesamtauswertung Kachel am Ende
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
# 2. EINTRAG ERSTELLEN (Kategorien-Ansicht)
# ----------------------------------------------------
elif (
    menu == "Eintrag erstellen (Kategorien)"
    or st.session_state.get("nav_override")
    == "Eintrag erstellen (Kategorien)"
):
  if "nav_override" in st.session_state:
    del st.session_state.nav_override

  st.title("Tagebuch")
  st.markdown("##### Wähle eine Kategorie für deinen Eintrag")
  st.write("---")

  col1, col2 = st.columns(2)

  selected_cat = None
  with col1:
    if st.button("🏃‍♂️ Ausdauer", use_container_width=True):
      selected_cat = "Ausdauer"
    if st.button("🚶‍♂️ Beweglichkeit", use_container_width=True):
      selected_cat = "Beweglichkeit"
    if st.button("🍽️ Ernährung", use_container_width=True):
      selected_cat = "Ernährung"

  with col2:
    if st.button("🏋️‍♂️ Kraft", use_container_width=True):
      selected_cat = "Kraft"
    if st.button("📋 Selbstmanagement", use_container_width=True):
      selected_cat = "Selbstmanagement"
    if st.button("😊 Gesamtbefinden", use_container_width=True):
      selected_cat = "Gesamtbefinden"

  if selected_cat:
    st.success(f"Kategorie ausgewählt: **{selected_cat}**")
    with st.form(key="kategorie_form"):
      st.subheader(f"Füge einen Eintrag für {selected_cat} hinzu")
      datum = st.date_input("Datum")
      minuten = st.number_input(
          "Minuten", min_value=0, max_value=300, value=30
      )
      notizen = st.text_input("Notizen / Details")

      save_btn = st.form_submit_button("Speichern")
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
        st.success("Eintrag erfolgreich gespeichert!")

  st.write("---")
  if st.button("⬅️ Zurück zur Startseite"):
    st.rerun()

# ----------------------------------------------------
# 3. ÜBUNGSARSENAL
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
