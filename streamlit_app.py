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
            "Balance",
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

    elif selected_cat == "Balance":
      selected_unterkat = st.selectbox(
          "Unterkategorie",
          BALANCE_UNTERKATEGORIEN,
          key="entry_unterkategorie",
      )
      selected_unterkat = handle_sonstiges_unterkategorie(
          selected_unterkat, "balance"
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

    verknuepfte_uebung = ""
    verknuepfter_link = ""
    verknuepftes_bild = ""
    passende_arsenal_eintraege = st.session_state.arsenal[
        st.session_state.arsenal["Kategorie"] == selected_cat
    ]
    if not passende_arsenal_eintraege.empty:
      arsenal_optionen = ["Keine Auswahl"] + passende_arsenal_eintraege[
          "Bereich / Übung"
      ].tolist()
      gewaehlte_uebung = st.selectbox(
          "🔗 Aus Übungsarsenal wählen (optional)", arsenal_optionen,
          key="entry_arsenal_auswahl",
      )
      if gewaehlte_uebung != "Keine Auswahl":
        arsenal_eintrag = passende_arsenal_eintraege[
            passende_arsenal_eintraege["Bereich / Übung"] == gewaehlte_uebung
        ].iloc[0]
        verknuepfte_uebung = gewaehlte_uebung
        verknuepfter_link = arsenal_eintrag.get("Link", "") or ""
        verknuepftes_bild = arsenal_eintrag.get("Bild", "") or ""
        if arsenal_eintrag.get("Beschreibung"):
          st.caption(arsenal_eintrag["Beschreibung"])
        if verknuepfter_link:
          st.markdown(f"🔗 [{verknuepfter_link}]({verknuepfter_link})")
        if verknuepftes_bild:
          st.image(verknuepftes_bild, use_container_width=True)

    datum = st.date_input("Datum", value=heute, key="entry_datum")
    notizen = st.text_input("Notizen / Details", key="entry_notizen")

    weitere_details_aktiv = st.checkbox(
        "➕ Weitere Details (Sätze, Wiederholungen, Dauer, Link, Bild)",
        key="entry_weitere_details_toggle",
    )
    wd_dauer = wd_saetze = wd_wiederholungen = None
    wd_link = ""
    wd_bild_upload = None
    if weitere_details_aktiv:
      with st.container(key="wd_details_row"):
        wd_col1, wd_col2, wd_col3 = st.columns(3)
        with wd_col1:
          wd_dauer = st.number_input(
              "Dauer (Minuten)", min_value=0, max_value=300, value=None,
              key="entry_wd_dauer",
          )
        with wd_col2:
          wd_saetze = st.number_input(
              "Sätze", min_value=0, max_value=50, value=None,
              key="entry_wd_saetze",
          )
        with wd_col3:
          wd_wiederholungen = st.number_input(
              "Wiederholungen", min_value=0, max_value=1000, value=None,
              key="entry_wd_wiederholungen",
          )
      wd_link = st.text_input("Link – optional", key="entry_wd_link")
      wd_bild_upload = st.file_uploader(
          "Bild – optional", type=["png", "jpg", "jpeg"],
          key="entry_wd_bild",
      )

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
              "Verknüpfte Übung": verknuepfte_uebung,
              "Verknüpfter Link": verknuepfter_link,
              "Verknüpftes Bild": verknuepftes_bild,
          }]
      )
      st.session_state.protokoll = pd.concat(
          [st.session_state.protokoll, neuer_eintrag], ignore_index=True
      )
      _speichere_nutzer_df("protokoll", st.session_state.protokoll)
      if weitere_details_aktiv:
        wd_bild_data_uri = ""
        if wd_bild_upload is not None:
          wd_bild_data_uri = _bild_datei_zu_data_uri(wd_bild_upload)
        neue_uebung = pd.DataFrame(
            [{
                "Datum": str(datum),
                "Kategorie": selected_cat,
                "Unterkategorie": selected_unterkat,
                "Dauer (Min.)": wd_dauer,
                "Sätze": wd_saetze,
                "Wiederholungen": wd_wiederholungen,
                "Notizen": notizen,
                "Link": wd_link.strip(),
                "Bild": wd_bild_data_uri,
            }]
        )
        st.session_state.eigene_uebungen = pd.concat(
            [st.session_state.eigene_uebungen, neue_uebung],
            ignore_index=True,
        )
        _speichere_nutzer_df(
            "eigene_uebungen", st.session_state.eigene_uebungen
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
            (f"{balance_icon_html(20)} Balance", "Balance"),
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

  def _vital_zeitraum_df(zeitraum):
    if vital_df.empty:
      return vital_df
    if zeitraum == "Woche":
      zeitraum_df = vital_df[
          (vital_df["Datum"] >= str(start_der_woche))
          & (vital_df["Datum"] <= str(ende_der_woche))
      ]
    else:
      zeitraum_tage = {
          "Monat": 30,
          "3 Monate": 90,
          "6 Monate": 180,
          "Jahr": 365,
      }[zeitraum]
      stichtag = str(heute - datetime.timedelta(days=zeitraum_tage))
      zeitraum_df = vital_df[vital_df["Datum"] >= stichtag]
    return zeitraum_df.sort_values("Datum")

  def _vital_zeitraum_avg(spalte, zeitraum):
    werte = _vital_zeitraum_df(zeitraum)[spalte].dropna()
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
  gewicht_heute = _vital_heute("Gewicht")
  vo2max_aktuell = _vital_letzter_wert("VO2max")

  if "koerpergroesse_cm" not in st.session_state:
    st.session_state.koerpergroesse_cm = _lade_koerpergroesse()

  with st.container(key="vitalcard"):
    st.subheader("📊 Vitalwerte")

    if st.session_state.koerpergroesse_cm is None:
      groesse_input = st.number_input(
          "Körpergröße (cm) – einmalig für BMI-Berechnung",
          min_value=0,
          max_value=250,
          value=None,
          key="groesse_input",
      )
      if groesse_input:
        st.session_state.koerpergroesse_cm = groesse_input
        _speichere_koerpergroesse(groesse_input)
        st.rerun()
    else:
      with st.expander(
          f"Körpergröße: {st.session_state.koerpergroesse_cm:.0f} cm "
          "(ändern)"
      ):
        groesse_input = st.number_input(
            "Körpergröße (cm) – einmalig für BMI-Berechnung",
            min_value=0,
            max_value=250,
            value=st.session_state.koerpergroesse_cm,
            key="groesse_input",
        )
        neue_groesse = groesse_input if groesse_input else None
        if neue_groesse != st.session_state.koerpergroesse_cm:
          st.session_state.koerpergroesse_cm = neue_groesse
          _speichere_koerpergroesse(neue_groesse)

    bmi_wert = None
    if gewicht_heute and st.session_state.koerpergroesse_cm:
      groesse_m = st.session_state.koerpergroesse_cm / 100
      bmi_wert = gewicht_heute / (groesse_m**2)

    zeitraum_auswahl = st.selectbox(
        "Zeitraum für die Ø-Werte",
        ["Woche", "Monat", "3 Monate", "6 Monate", "Jahr"],
        key="vital_zeitraum_auswahl",
    )
    schritte_zeitraum_avg = _vital_zeitraum_avg("Schritte", zeitraum_auswahl)
    gewicht_zeitraum_avg = _vital_zeitraum_avg("Gewicht", zeitraum_auswahl)

    with st.container(key="vital_metrics_row"):
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
            f"Ø Schritte/Tag ({zeitraum_auswahl})",
            f"{int(schritte_zeitraum_avg):,}".replace(",", ".")
            if schritte_zeitraum_avg is not None
            else "–",
        )
      with m_col3:
        st.metric(
            "Gewicht heute in kg",
            f"{gewicht_heute:.1f}" if gewicht_heute is not None else "–",
        )
      with m_col4:
        st.metric(
            f"Ø Gewicht ({zeitraum_auswahl}) in kg",
            f"{gewicht_zeitraum_avg:.1f}"
            if gewicht_zeitraum_avg is not None
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
    st.markdown(f"#### 📈 Verlauf ({zeitraum_auswahl})")
    verlauf_df = _vital_zeitraum_df(zeitraum_auswahl)
    if verlauf_df.empty:
      st.info("Noch keine Einträge für diesen Zeitraum.")
    else:
      chart_col1, chart_col2 = st.columns(2)
      with chart_col1:
        st.caption("Schritte")
        schritte_verlauf = verlauf_df.dropna(subset=["Schritte"])
        if schritte_verlauf.empty:
          st.info("Keine Schritte-Einträge in diesem Zeitraum.")
        else:
          st.line_chart(
              schritte_verlauf.set_index("Datum")["Schritte"],
              height=220,
          )
      with chart_col2:
        st.caption("Gewicht (kg)")
        gewicht_verlauf = verlauf_df.dropna(subset=["Gewicht"])
        if gewicht_verlauf.empty:
          st.info("Keine Gewicht-Einträge in diesem Zeitraum.")
        else:
          gewicht_chart = (
              alt.Chart(gewicht_verlauf)
              .mark_line(point=True)
              .encode(
                  x=alt.X("Datum:T", title=None),
                  y=alt.Y(
                      "Gewicht:Q",
                      title=None,
                      scale=alt.Scale(domain=[40, 90]),
                  ),
              )
              .properties(height=220)
          )
          st.altair_chart(gewicht_chart, width="stretch")

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
        _speichere_nutzer_df("vitaldaten", st.session_state.vitaldaten)
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
            _speichere_nutzer_df("vitaldaten", st.session_state.vitaldaten)
            st.session_state.vital_import_aktiv = False
            st.success(f"{len(neue_zeilen)} Zeilen importiert!")
            st.rerun()
        except Exception as e:
          st.error(f"CSV konnte nicht gelesen werden: {e}")

      if st.button("Abbrechen", key="vital_import_cancel_btn"):
        st.session_state.vital_import_aktiv = False
        st.rerun()

  st.write("---")
  st.write("### 📒 Ergänzende Trainingsnotizen")

  UEBUNG_UNTERKATEGORIEN = {
      "Ausdauer": AUSDAUER_UNTERKATEGORIEN,
      "Kraft": KRAFT_UNTERKATEGORIEN,
      "Beweglichkeit": BEWEGLICHKEIT_UNTERKATEGORIEN,
      "Balance": BALANCE_UNTERKATEGORIEN,
      "Ernährung": ERNAEHRUNG_UNTERKATEGORIEN,
      "Gesamtbefinden": GESAMTBEFINDEN_UNTERKATEGORIEN,
  }

  tab_protokoll, tab_uebungen = st.tabs(
      ["Tagebuch-Einträge", "Eigene Übungen (Name, Sätze, Wiederholungen, Dauer)"]
  )

  with tab_protokoll:
    if not df.empty:
      st.markdown("#### 🔍 Tagebuch filtern")
      with st.container(key="protokoll_filter_row"):
        p_col1, p_col2, p_col3 = st.columns(3)
        with p_col1:
          p_kategorie = st.selectbox(
              "Kategorie", ["Alle Kategorien"] + ARSENAL_KATEGORIEN,
              key="protokoll_filter_kategorie",
          )
        with p_col2:
          if p_kategorie == "Alle Kategorien":
            p_unterkategorie_optionen = sorted(
                df["Unterkategorie"].dropna().unique().tolist()
            )
          else:
            p_unterkategorie_optionen = UEBUNG_UNTERKATEGORIEN.get(
                p_kategorie, []
            )
          p_unterkategorie = st.selectbox(
              "Unterkategorie",
              ["Alle Unterkategorien"] + list(p_unterkategorie_optionen),
              key="protokoll_filter_unterkategorie",
          )
        with p_col3:
          p_zeitraum = st.selectbox(
              "Zeitraum",
              ["Alle", "Heute", "Letzte Woche", "Letzter Monat",
               "Letzte 3 Monate", "Letztes Jahr"],
              key="protokoll_filter_zeitraum",
          )

      gefilterter_df = df.copy()
      if p_kategorie != "Alle Kategorien":
        gefilterter_df = gefilterter_df[
            gefilterter_df["Kategorie"] == p_kategorie
        ]
      if p_unterkategorie != "Alle Unterkategorien":
        gefilterter_df = gefilterter_df[
            gefilterter_df["Unterkategorie"] == p_unterkategorie
        ]
      if p_zeitraum == "Heute":
        gefilterter_df = gefilterter_df[gefilterter_df["Datum"] == str(heute)]
      elif p_zeitraum != "Alle":
        zeitraum_tage = {
            "Letzte Woche": 7,
            "Letzter Monat": 30,
            "Letzte 3 Monate": 90,
            "Letztes Jahr": 365,
        }[p_zeitraum]
        stichtag = str(heute - datetime.timedelta(days=zeitraum_tage))
        gefilterter_df = gefilterter_df[gefilterter_df["Datum"] >= stichtag]

      st.caption(f"{len(gefilterter_df)} von {len(df)} Einträgen")
      st.dataframe(
          gefilterter_df.sort_values("Datum", ascending=False),
          use_container_width=True,
          column_config={
              "Verknüpftes Bild": st.column_config.ImageColumn(
                  "Verknüpftes Bild"
              ),
              "Verknüpfter Link": st.column_config.LinkColumn(
                  "Verknüpfter Link"
              ),
          },
      )

      @st.cache_data
      def convert_df_to_excel(dataframe):
        from io import BytesIO

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
          dataframe.to_excel(writer, index=False, sheet_name="Protokoll")
        return output.getvalue()

      excel_data = convert_df_to_excel(gefilterter_df)
      st.download_button(
          label="📥 Als Excel-Datei herunterladen",
          data=excel_data,
          file_name="Sport_Tagebuch.xlsx",
          mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      )
    else:
      st.info("Noch keine Einträge vorhanden.")

  with tab_uebungen:
    st.caption(
        "Alle Übungen an einem Ort: Kategorie, Unterkategorie, Sätze/"
        " Wiederholungen, Dauer, Notizen, Link und Bild."
    )

    col_u1, col_u2 = st.columns(2)
    with col_u1:
      if st.button(
          "＋ Übung erfassen", key="btn_open_uebung_form",
          type="primary", use_container_width=True,
      ):
        st.session_state.eigene_uebung_form_aktiv = True
        st.session_state.eigene_uebung_import_aktiv = False
        st.rerun()
    with col_u2:
      if st.button(
          "⬆️ Excel importieren", key="btn_open_uebung_import",
          use_container_width=True,
      ):
        st.session_state.eigene_uebung_import_aktiv = True
        st.session_state.eigene_uebung_form_aktiv = False
        st.rerun()

    if st.session_state.eigene_uebung_form_aktiv:
      st.write("---")
      u_kategorie = st.selectbox(
          "Kategorie", list(UEBUNG_UNTERKATEGORIEN.keys()),
          key="uebung_kategorie_input",
      )
      u_unterkategorie = st.selectbox(
          "Unterkategorie", UEBUNG_UNTERKATEGORIEN[u_kategorie],
          key=f"uebung_unterkategorie_input_{u_kategorie}",
      )
      u_unterkategorie = handle_sonstiges_unterkategorie(
          u_unterkategorie, f"uebung_{u_kategorie}"
      )
      u_datum = st.date_input("Datum", value=heute, key="uebung_datum_input")
      u_dauer = st.number_input(
          "Dauer (Minuten) – optional", min_value=0, max_value=300,
          value=None, key="uebung_dauer_input",
      )
      u_saetze = st.number_input(
          "Sätze – optional", min_value=0, max_value=50, value=None,
          key="uebung_saetze_input",
      )
      u_wiederholungen = st.number_input(
          "Wiederholungen – optional", min_value=0, max_value=1000,
          value=None, key="uebung_wiederholungen_input",
      )
      u_notizen = st.text_input("Notizen", key="uebung_notizen_input")
      u_link = st.text_input("Link – optional", key="uebung_link_input")
      u_bild_upload = st.file_uploader(
          "Bild – optional", type=["png", "jpg", "jpeg"],
          key="uebung_bild_input",
      )

      col_us1, col_us2 = st.columns(2)
      with col_us1:
        uebung_save = st.button(
            "Speichern", key="uebung_save_btn", type="primary",
            use_container_width=True,
        )
      with col_us2:
        uebung_cancel = st.button(
            "Abbrechen", key="uebung_cancel_btn", use_container_width=True
        )
      if uebung_save:
        u_bild_data_uri = ""
        if u_bild_upload is not None:
          u_bild_data_uri = _bild_datei_zu_data_uri(u_bild_upload)

        neue_uebung = pd.DataFrame(
            [{
                "Datum": str(u_datum),
                "Kategorie": u_kategorie,
                "Unterkategorie": u_unterkategorie,
                "Dauer (Min.)": u_dauer,
                "Sätze": u_saetze,
                "Wiederholungen": u_wiederholungen,
                "Notizen": u_notizen.strip(),
                "Link": u_link.strip(),
                "Bild": u_bild_data_uri,
            }]
        )
        st.session_state.eigene_uebungen = pd.concat(
            [st.session_state.eigene_uebungen, neue_uebung],
            ignore_index=True,
        )
        _speichere_nutzer_df(
            "eigene_uebungen", st.session_state.eigene_uebungen
        )
        st.session_state.eigene_uebung_form_aktiv = False
        st.success("Gespeichert!")
        st.rerun()
      if uebung_cancel:
        st.session_state.eigene_uebung_form_aktiv = False
        st.rerun()

    if st.session_state.eigene_uebung_import_aktiv:
      st.write("---")
      st.caption(
          "Lade eine Excel-Datei mit deinen eigenen Übungen hoch (z.B."
          " Export aus einer Trainings-App oder einer eigenen Tabelle)."
      )
      excel_upload = st.file_uploader(
          "Excel-Datei auswählen", type=["xlsx", "xls"],
          key="uebung_excel_upload",
      )
      if excel_upload is not None:
        try:
          import_df = pd.read_excel(excel_upload)
          st.write("Vorschau:")
          st.dataframe(import_df.head(), use_container_width=True)

          spalten = import_df.columns.tolist()
          keine_option = "– keine –"
          u_datum_spalte = st.selectbox(
              "Welche Spalte enthält das Datum?", spalten,
              key="uebung_import_datum_spalte",
          )
          u_kategorie_spalte = st.selectbox(
              "Welche Spalte enthält die Kategorie?", spalten,
              key="uebung_import_kategorie_spalte",
          )
          u_unterkategorie_spalte = st.selectbox(
              "Welche Spalte enthält die Unterkategorie?",
              [keine_option] + spalten,
              key="uebung_import_unterkategorie_spalte",
          )
          u_dauer_spalte = st.selectbox(
              "Welche Spalte enthält die Dauer in Minuten? (optional)",
              [keine_option] + spalten, key="uebung_import_dauer_spalte",
          )
          u_saetze_spalte = st.selectbox(
              "Welche Spalte enthält die Sätze? (optional)",
              [keine_option] + spalten, key="uebung_import_saetze_spalte",
          )
          u_wdh_spalte = st.selectbox(
              "Welche Spalte enthält die Wiederholungen? (optional)",
              [keine_option] + spalten, key="uebung_import_wdh_spalte",
          )
          u_notizen_spalte = st.selectbox(
              "Welche Spalte enthält Notizen? (optional)",
              [keine_option] + spalten, key="uebung_import_notizen_spalte",
          )
          u_link_spalte = st.selectbox(
              "Welche Spalte enthält den Link? (optional)",
              [keine_option] + spalten, key="uebung_import_link_spalte",
          )

          if st.button(
              "Importieren", key="uebung_import_btn", type="primary"
          ):
            neue_zeilen = pd.DataFrame()
            neue_zeilen["Datum"] = pd.to_datetime(
                import_df[u_datum_spalte], errors="coerce"
            ).dt.strftime("%Y-%m-%d")
            neue_zeilen["Kategorie"] = import_df[u_kategorie_spalte]
            neue_zeilen["Unterkategorie"] = (
                import_df[u_unterkategorie_spalte]
                if u_unterkategorie_spalte != keine_option
                else ""
            )
            neue_zeilen["Dauer (Min.)"] = (
                pd.to_numeric(import_df[u_dauer_spalte], errors="coerce")
                if u_dauer_spalte != keine_option
                else None
            )
            neue_zeilen["Sätze"] = (
                pd.to_numeric(import_df[u_saetze_spalte], errors="coerce")
                if u_saetze_spalte != keine_option
                else None
            )
            neue_zeilen["Wiederholungen"] = (
                pd.to_numeric(import_df[u_wdh_spalte], errors="coerce")
                if u_wdh_spalte != keine_option
                else None
            )
            neue_zeilen["Notizen"] = (
                import_df[u_notizen_spalte]
                if u_notizen_spalte != keine_option
                else ""
            )
            neue_zeilen["Link"] = (
                import_df[u_link_spalte]
                if u_link_spalte != keine_option
                else ""
            )
            neue_zeilen["Bild"] = ""
            neue_zeilen = neue_zeilen.dropna(subset=["Datum", "Kategorie"])
            st.session_state.eigene_uebungen = pd.concat(
                [st.session_state.eigene_uebungen, neue_zeilen],
                ignore_index=True,
            )
            _speichere_nutzer_df(
                "eigene_uebungen", st.session_state.eigene_uebungen
            )
            st.session_state.eigene_uebung_import_aktiv = False
            st.success(f"{len(neue_zeilen)} Zeilen importiert!")
            st.rerun()
        except Exception as e:
          st.error(f"Excel-Datei konnte nicht gelesen werden: {e}")

      if st.button("Abbrechen", key="uebung_import_cancel_btn"):
        st.session_state.eigene_uebung_import_aktiv = False
        st.rerun()

    uebungen_df = st.session_state.eigene_uebungen
    if uebungen_df.empty:
      st.info("Noch keine eigenen Übungen erfasst.")
    else:
      uebungen_kategorien = list(UEBUNG_UNTERKATEGORIEN.keys())
      uebungen_icons = {
          "Ausdauer": "🏃‍♂️",
          "Kraft": "🏋️‍♂️",
          "Beweglichkeit": beweglichkeit_icon_html(26),
          "Balance": balance_icon_html(26),
          "Ernährung": "🍽️",
          "Gesamtbefinden": "😊",
      }

      u_kat_col1, u_kat_col2, u_kat_col3, u_kat_col4, u_kat_col5, u_kat_col6 = (
          st.columns(6)
      )
      for spalte, kat in zip(
          [u_kat_col1, u_kat_col2, u_kat_col3, u_kat_col4, u_kat_col5,
           u_kat_col6],
          uebungen_kategorien,
      ):
        with spalte:
          anzahl = len(uebungen_df[uebungen_df["Kategorie"] == kat])
          render_arsenal_tile(
              uebungen_icons.get(kat, "📌"), kat, anzahl,
              state_key="uebungen_detail_kat", button_prefix="uebungtile",
          )

      # Detail-Liste für die angeklickte Kategorie
      aktive_uebungen_kat = st.session_state.get("uebungen_detail_kat")
      if aktive_uebungen_kat is not None:
        kat_eintraege = uebungen_df[
            uebungen_df["Kategorie"] == aktive_uebungen_kat
        ]
        st.write("---")
        st.markdown(f"#### {aktive_uebungen_kat} ({len(kat_eintraege)})")
        if kat_eintraege.empty:
          st.info(f"Noch keine Einträge für {aktive_uebungen_kat}.")
        else:
          anzeige_spalten = [
              c
              for c in [
                  "Datum", "Unterkategorie", "Dauer (Min.)", "Sätze",
                  "Wiederholungen", "Notizen", "Link", "Bild",
              ]
              if c in kat_eintraege.columns
          ]
          st.dataframe(
              kat_eintraege[anzeige_spalten].sort_values("Datum"),
              use_container_width=True,
              hide_index=True,
              column_config={
                  "Bild": st.column_config.ImageColumn("Bild"),
                  "Link": st.column_config.LinkColumn("Link"),
              },
          )
        if st.button("✕ Schließen", key="uebungen_detail_schliessen_btn"):
          st.session_state["uebungen_detail_kat"] = None
          st.rerun()

      # Falls Einträge eine Kategorie außerhalb der Standardliste haben
      sonstige_uebungen = uebungen_df[
          ~uebungen_df["Kategorie"].isin(uebungen_kategorien)
      ]
      if not sonstige_uebungen.empty:
        with st.expander(f"Sonstige Kategorien ({len(sonstige_uebungen)})"):
          st.dataframe(
              sonstige_uebungen,
              use_container_width=True,
              column_config={
                  "Bild": st.column_config.ImageColumn("Bild"),
                  "Link": st.column_config.LinkColumn("Link"),
              },
          )

      st.write("---")
      st.markdown("#### 🔍 Trainingsnotizen filtern")
      with st.container(key="uebungen_filter_row"):
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
          f_kategorie = st.selectbox(
              "Kategorie", ["Alle Kategorien"] + uebungen_kategorien,
              key="uebungen_filter_kategorie",
          )
        with f_col2:
          if f_kategorie == "Alle Kategorien":
            f_unterkategorie_optionen = sorted(
                uebungen_df["Unterkategorie"].dropna().unique().tolist()
            )
          else:
            f_unterkategorie_optionen = UEBUNG_UNTERKATEGORIEN.get(
                f_kategorie, []
            )
          f_unterkategorie = st.selectbox(
              "Unterkategorie",
              ["Alle Unterkategorien"] + list(f_unterkategorie_optionen),
              key="uebungen_filter_unterkategorie",
          )
        with f_col3:
          f_zeitraum = st.selectbox(
              "Zeitraum",
              ["Alle", "Letzte Woche", "Letzter Monat", "Letztes Jahr"],
              key="uebungen_filter_zeitraum",
          )

      gefilterte_df = uebungen_df.copy()
      if f_kategorie != "Alle Kategorien":
        gefilterte_df = gefilterte_df[
            gefilterte_df["Kategorie"] == f_kategorie
        ]
      if f_unterkategorie != "Alle Unterkategorien":
        gefilterte_df = gefilterte_df[
            gefilterte_df["Unterkategorie"] == f_unterkategorie
        ]
      if f_zeitraum != "Alle":
        zeitraum_tage = {
            "Letzte Woche": 7,
            "Letzter Monat": 30,
            "Letztes Jahr": 365,
        }[f_zeitraum]
        stichtag = str(heute - datetime.timedelta(days=zeitraum_tage))
        gefilterte_df = gefilterte_df[gefilterte_df["Datum"] >= stichtag]

      st.caption(f"{len(gefilterte_df)} von {len(uebungen_df)} Einträgen")
      if gefilterte_df.empty:
        st.info("Keine Einträge für die gewählten Filter gefunden.")
      else:
        f_anzeige_spalten = [
            c
            for c in [
                "Datum", "Kategorie", "Unterkategorie", "Dauer (Min.)",
                "Sätze", "Wiederholungen", "Notizen", "Link", "Bild",
            ]
            if c in gefilterte_df.columns
        ]
        st.dataframe(
            gefilterte_df[f_anzeige_spalten].sort_values(
                "Datum", ascending=False
            ),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Bild": st.column_config.ImageColumn("Bild"),
                "Link": st.column_config.LinkColumn("Link"),
            },
        )

      st.write("")

      @st.cache_data
      def convert_uebungen_df_to_excel(dataframe):
        from io import BytesIO

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
          dataframe.to_excel(
              writer, index=False, sheet_name="Eigene Übungen"
          )
        return output.getvalue()

      uebungen_excel_data = convert_uebungen_df_to_excel(uebungen_df)
      st.download_button(
          label="📥 Als Excel-Datei herunterladen",
          data=uebungen_excel_data,
          file_name="Eigene_Uebungen.xlsx",
          mime=(
              "application/vnd.openxmlformats-officedocument"
              ".spreadsheetml.sheet"
          ),
          key="uebungen_download_btn",
      )

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
          "Beweglichkeit": beweglichkeit_icon_html(26),
          "Balance": balance_icon_html(26),
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
          bild_data_uri = _bild_datei_zu_data_uri(bild_upload)

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
        _speichere_nutzer_df("arsenal", st.session_state.arsenal)
        st.session_state.arsenal_form_aktiv = False
        st.success("Erfolgreich hinzugefügt!")
        st.rerun()
      if arsenal_cancelled:
        st.session_state.arsenal_form_aktiv = False
        st.rerun()
