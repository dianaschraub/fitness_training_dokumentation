# 6 Kategorien im Kachel-Stil anzeigen (2 Spalten)
kategorien_liste = [
    ("🏃‍♂️ Ausdauer", "Ausdauer"),
    ("🏋️‍♂️ Kraft", "Kraft"),
    ("🚶‍♂️ Beweglichkeit", "Beweglichkeit"),
    ("📋 Selbstmanagement", "Selbstmanagement"),
    ("🍽️ Ernährung", "Ernährung"),
    ("😊 Gesamtbefinden", "Gesamtbefinden"),
]

col_c1, col_c2 = st.columns(2)
for i, (titel, kat_key) in enumerate(kategorien_liste):
  minuten_val, status_text, symbol = get_cat_stats(kat_key)
  target_col = col_c1 if i % 2 == 0 else col_c2
  with target_col:
    st.markdown(
        f"""
            <div style="padding: 15px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 10px; background-color: #f9f9f9;">
                <h4 style="margin: 0; color: #333;">{titel}</h4>
                <p style="margin: 5px 0 0 0; font-size: 14px; color: #666;">{symbol} {status_text}</p>
            </div>
            """,
        unsafe_allow_html=True,
    )
