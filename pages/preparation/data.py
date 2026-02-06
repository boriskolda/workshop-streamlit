import streamlit as st
import pandas as pd

st.title("💾 Cvičný dataset")
st.markdown("""
Pro účely workshopu budeme pracovat s **reálnými daty Českého statistického úřadu**.
Konkrétně se jedná o **Indexy spotřebitelských cen (míra inflace)**.
""")

st.info("Zdroj: [ČSÚ - Indexy spotřebitelských cen](https://data.gov.cz/datová-sada?iri=https%3A%2F%2Fdata.gov.cz%2Fzdroj%2Fdatové-sady%2F00025593%2F790624c7263aca615ce9ddd24e7db464)")

st.divider()

# --- CVIČNÝ DATASET ---
st.header("Dataset pro workshop: `010022-25.csv`")
st.markdown("""
Tento soubor je již součástí projektu ve složce `data/`. Můžete si ho zde stáhnout pro kontrolu.
Obsahuje vývoj inflace pro různé kategorie zboží a služeb.
""")

# Načtení dat pro download button
@st.cache_data
def load_csv():
    df = pd.read_csv("data/010022-25.csv")
    return df.to_csv(index=False).encode('utf-8-sig')

try:
    csv_data = load_csv()
    st.download_button(
        label="📥 Stáhnout data o inflaci (CSV)",
        data=csv_data,
        file_name="inflace.csv",
        mime="text/csv",
        type="primary"
    )
except FileNotFoundError:
    st.error("Soubor data/010022-25.csv nebyl nalezen.")

st.divider()

st.header("Alternativní zdroje")
st.markdown("Pokud byste si chtěli vyzkoušet analýzu na jiných datech:")
# ... (zbytek souboru s odkazy na Kaggle atd. zůstává)
c1, c2, c3 = st.columns(3)
with c1:
    st.subheader("🌍 Světová data")
    st.markdown("**[Kaggle Datasets](https://www.kaggle.com/datasets)**")
with c2:
    st.subheader("🇨🇿 Česká data")
    st.markdown("**[Data.gov.cz](https://data.gov.cz/)**")
with c3:
    st.subheader("📈 Statistiky")
    st.markdown("**[Our World in Data](https://ourworldindata.org/)**")
