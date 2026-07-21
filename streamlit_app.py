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
# 1. STARTSEITE & TAGEBUCH (mit automatischem Datum)
# ----------------------------------------------------
if menu == "Startseite & Tagebuch":
  st.title("Tagebuch")
  st.markdown("##### Aktivitätentagebuch Prävention")
  st.write("---")

  # --- Automatische Datums- und Wochenberechnung ---
  heute = datetime.date.today()
  jahr, kalenderwoche, wochentag = heute.isocalendar()

  # Montag und Sonntag der aktuellen Woche berechnen
  start_der_woche = heute - datetime.timedelta(days=wochentag - 1)
  ende_der_woche = start_der_woche + datetime.timedelta(days=6)

  # Monate für die deutsche Anzeige formatieren
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
  # -------------------------------------------------

  # Wochen-Kopfzeile mit den berechneten Werten
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

  # Gesamtminuten aus Protokoll berechnen
  if not st.session_state.protokoll.empty:
    gesamt_minuten = st.session_state.protokoll["Minuten"].sum()
  else:
    gesamt_minuten = 0

  # Ampel-Logik für Startseite (Grün >= 90, Gelb >= 60, Rot < 60)
  if gesamt_minuten >= 90:
    status_text = "🟢 Ausreichend (Grün)"
  elif gesamt_minuten >= 60:
    status_text = "🟡 Mittel (Gelb)"
  else:
    status_text = "🔴 Zu wenig (Rot)"

  # Infobox
  st.info(
      f"**Wochenstatus:** {gesamt_minuten} Minuten trainiert — **Status:**"
      f" {status_text}"
  )

  # Button "Eintrag erstellen" auf der Startseite
  st.write("")
  if st.button("➕ Eintrag erstellen", use_container_width=True, type="primary"):
    st.session_state.nav_override = "Eintrag erstellen (Kategorien)"
    st.rerun()

  st.write("---")
  st.write("### Bisherige Einträge dieser Woche")
  if not st.session_state.protokoll.empty:
    st.dataframe(st.session_state.protokoll, use_container_width=True)

    # Excel-Export Button
    @st.cache_data
    def convert_df_to_excel(df):
      from io import BytesIO

      output = BytesIO()
      with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Protokoll")
      return output.getvalue()

    excel_data = convert_df_to_excel(st.session_state.protokoll)
    st.download_button(
        label="📥 Als Excel-Datei herunterladen",
        data=excel_data,
        file_name="Sport_Tagebuch.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
  else:
    st.write("Noch keine Einträge vorhanden. Starte mit 'Eintrag erstellen'.")

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
      st.subheader(f"Eintrag für {selected_cat} erfassen")
      datum = st.date_input("Datum")
      minuten = st.number_input(
          "Minuten (falls zutreffend)", min_value=0, max_value=300, value=30
      )
      status_bewertung = st.selectbox(
          "Bewertung / Status",
          [
              "Gut (Grün)",
              "Teilweise umgesetzt (Gelb)",
              "Verbesserungsbedarf (Rot)",
          ],
      )
      notizen = st.text_input("Notizen / Details")

      save_btn = st.form_submit_button("Speichern")
      if save_btn:
        neuer_eintrag = pd.DataFrame(
            [{
                "Datum": str(datum),
                "Kategorie": selected_cat,
                "Minuten": minuten,
                "Status": status_bewertung,
                "Notizen": notizen,
            }]
        )
        st.session_state.protokoll = pd.concat(
            [st.session_state.protokoll, neuer_eintrag], ignore_index=True
        )
        st.success("Eintrag erfolgreich gespeichert!")
        st.balloons()

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

