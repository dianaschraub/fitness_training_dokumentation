import pandas as pd
import streamlit as st

# Seiten-Konfiguration
st.set_page_config(
    page_title="Sport-Tagebuch", page_icon="🏃‍♀️", layout="centered"
)

# Initialisierung des Session State für Daten, falls noch nicht vorhanden
if "protokoll" not in st.session_state:
    st.session_state.protokoll = pd.DataFrame(
        columns=["Datum", "Sportart", "Minuten", "Intensität", "Notizen"]
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
    ["Startseite & Dashboard", "Eintrag erstellen", "Übungsarsenal"],
)

# ----------------------------------------------------
# 1. STARTSEITE & DASHBOARD
# ----------------------------------------------------
if menu == "Startseite & Dashboard":
  st.title("Herzlich willkommen Diana Schraub")
  st.subheader("Wochen-Tagebuch & Aktivitäts-Übersicht")

  # Berechnung der Gesamtminuten (aus dem Session State)
  if not st.session_state.protokoll.empty:
    gesamt_minuten = st.session_state.protokoll["Minuten"].sum()
    anzahl_einheiten = len(st.session_state.protokoll)
  else:
    gesamt_minuten = 0
    anzahl_einheiten = 0

  # Kennzahlen anzeigen
  col1, col2 = st.columns(2)
  col1.metric("Gesamtminuten", f"{gesamt_minuten} Min")
  col2.metric("Anzahl Einheiten", anzahl_einheiten)

  # Ampel-Logik (Grün >= 90, Gelb >= 60, Rot < 60)
  st.write("### Status deines Wochenziels")
  if gesamt_minuten >= 90:
    st.success("🟢 Ausreichend (Grün) – Ziel erreicht!")
  elif gesamt_minuten >= 60:
    st.warning("🟡 Mittel (Gelb) – Weiter so!")
  else:
    st.danger("🔴 Zu wenig (Rot) – Da geht noch was!")

  # Bisheriges Protokoll anzeigen
  st.write("### Bisheriges Protokoll")
  if not st.session_state.protokoll.empty:
    st.dataframe(st.session_state.protokoll, use_container_width=True)

    # Excel-Export Button
    @st.cache_data
    def convert_df_to_excel(df):
      from io import BytesIO

      output = BytesIO()
      with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Protokoll")
      processed_data = output.getvalue()
      return processed_data

    excel_data = convert_df_to_excel(st.session_state.protokoll)
    st.download_button(
        label="📥 Als Excel-Datei herunterladen",
        data=excel_data,
        file_name="Sport_Protokoll.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
  else:
    st.info("Noch keine Aktivitäten eingetragen.")

# ----------------------------------------------------
# 2. EINTRAG ERSTELLEN
# -----------------
elif menu == "Eintrag erstellen":
  st.title("Neuen Eintrag erstellen")
  st.write("Trage hier deine sportliche Aktivität ein.")

  with st.form("eintrag_form"):
    datum = st.date_input("Datum")
    sportart = st.selectbox(
        "Sportart", ["Laufen", "Krafttraining", "Yoga", "Schwimmen", "Radfahren"]
    )
    minuten = st.number_input("Minuten", min_value=1, max_value=600, value=30)
    intensitaet = st.selectbox("Intensität", ["Leicht", "Mittel", "Hoch"])
    notizen = st.text_input("Notizen / Strecke")

    submitted = st.form_submit_button("Eintrag speichern")
    if submitted:
      neuer_eintrag = pd.DataFrame(
          [{
              "Datum": str(datum),
              "Sportart": sportart,
              "Minuten": minuten,
              "Intensität": intensitaet,
              "Notizen": notizen,
          }]
      )
      st.session_state.protokoll = pd.concat(
          [st.session_state.protokoll, neuer_eintrag], ignore_index=True
      )
      st.success("Aktivität erfolgreich gespeichert!")

# ----------------------------------------------------
# 3. ÜBUNGSARSENAL
# ----------------------------------------------------
elif menu == "Übungsarsenal":
  st.title("🏋️‍♀️ Übungsarsenal")
  st.write(
      "Deine Sammlung von Links zu Bereichen, Übungs-Hinweisen und Bildern."
  )

  # Anzeige der Tabelle
  st.dataframe(st.session_state.arsenal, use_container_width=True)

  st.write("---")
  st.subheader("Neuen Eintrag hinzufügen")
  with st.form("arsenal_form"):
    titel = st.text_input("Bereich oder Übung")
    kategorie = st.selectbox("Kategorie", ["Bereich", "Übung"])
    link = st.text_input("Link / URL (z.B. zu Video oder Anleitung)")
    beschreibung = st.text_area("Beschreibung / Notiz")

    arsenal_submitted = st.form_submit_button("Zum Arsenal hinzufügen")
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
      st.success("Erfolgreich zum Übungsarsenal hinzugefügt!")
