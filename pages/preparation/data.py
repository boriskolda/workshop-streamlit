import streamlit as st
import pandas as pd

st.title("💾 Výběr dat")
st.markdown("""
Pro účely workshopu budeme pracovat s **reálnými daty Českého statistického úřadu**.
Konkrétně se jedná o **Průměrné spotřebitelské ceny pohonných hmot (měsíční)**.
""")

st.info("Zdroj: [ČSÚ - Průměrné spotřebitelské ceny pohonných hmot (měsíční)](https://data.gov.cz/datová-sada?iri=https%3A%2F%2Fdata.gov.cz%2Fzdroj%2Fdatové-sady%2F00025593%2F4080dc3fb45edd7cf22a7e53fceb23a1)")

st.divider()

# --- CVIČNÝ DATASET ---
st.header("Dataset pro workshop: `CEN0101J.csv`")
st.markdown("""
Tento soubor je již součástí projektu ve složce `data/`. Můžete si ho zde stáhnout pro kontrolu.
Obsahuje měsíční vývoj cen různých druhů paliv v ČR od roku 2001.
""")

# Načtení dat pro download button
@st.cache_data
def load_csv():
    df = pd.read_csv("data/CEN0101J.csv")
    return df.to_csv(index=False).encode('utf-8-sig')

try:
    csv_data = load_csv()
    st.download_button(
        label="📥 Stáhnout data o cenách PHM (CSV)",
        data=csv_data,
        file_name="CEN0101J.csv",
        mime="text/csv",
        type="primary"
    )
except FileNotFoundError:
    st.error("Soubor data/CEN0101J.csv nebyl nalezen.")

st.divider()

st.header("Alternativní zdroje")
st.markdown("Pokud byste si chtěli vyzkoušet analýzu na jiných datech, zde je pár tipů:")

c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("🌍 Světová data")
    st.markdown("**[Kaggle Datasets](https://www.kaggle.com/datasets)**")
    st.caption("Obrovská databáze všeho možného. Nutná registrace.")
    st.markdown("""
    *   [Titanic](https://www.kaggle.com/c/titanic/data) (Kdo přežil?)
    *   [Netflix Movies](https://www.kaggle.com/shivamb/netflix-shows) (Co sledovat?)
    *   [Airbnb NYC](https://www.kaggle.com/dgomonov/new-york-city-airbnb-open-data) (Ceny ubytování)
    """)

with c2:
    st.subheader("🇨🇿 Česká data")
    st.markdown("**[Data.gov.cz](https://data.gov.cz/)**")
    st.caption("Oficiální otevřená data ČR.")
    st.markdown("""
    *   [Dopravní nehody](https://data.gov.cz/datová-sada?iri=https%3A%2F%2Fdata.gov.cz%2Fzdroj%2Fdatové-sady%2F00007064%2F853503930)
    *   [Volby](https://www.volby.cz/opendata/opendata.htm)
    *   [ČSÚ (Statistiky)](https://www.czso.cz/csu/czso/otevrena_data) (Mzdy, Inflace)
    """)

with c3:
    st.subheader("📈 Statistiky")
    st.markdown("**[Our World in Data](https://ourworldindata.org/)**")
    st.caption("Kvalitní globální statistiky v CSV.")
    st.markdown("""
    *   [CO2 a Klima](https://github.com/owid/co2-data)
    *   [Energie](https://github.com/owid/energy-data)
    *   [Populace](https://ourworldindata.org/population-growth)
    """)
