import streamlit as st
import pandas as pd

st.title("💾 Výběr dat")
st.markdown("""
Abychom mohli tvořit dashboard, potřebujeme data. Na workshopu máte **3 možnosti**, jaká data použít.
Vyberte si tu, která vám nejvíce vyhovuje.
""")

st.divider()

# --- MOŽNOST 1: VLASTNÍ DATA ---
st.header("1. Vlastní data (Doporučeno)")
st.info("🏆 **Nejlepší volba:** Pokud máte data z práce, školy nebo vlastního projektu, použijte je! Naučíte se nejvíc.")
st.markdown("""
**Požadavky na data:**
*   Formát **CSV** nebo **Excel**.
*   Ideálně "tabulková data" (řádky = záznamy, sloupce = vlastnosti).
*   Neměla by být příliš citlivá (GDPR), pokud je plánujete nahrát na veřejný GitHub.
""")

st.divider()

# --- MOŽNOST 2: CVIČNÝ DATASET ---
st.header("2. Náš cvičný dataset")
st.markdown("""
Pokud nemáte vlastní data, připravili jsme pro vás fiktivní dataset **Prodeje e-shopu**.
Obsahuje cca 2000 řádků (elektronika, nábytek, domácnost) s reálnou strukturou.
""")

# Načtení dat pro download button
@st.cache_data
def load_csv():
    df = pd.read_csv("data/prodeje.csv")
    return df.to_csv(index=False).encode('utf-8-sig')

try:
    csv_data = load_csv()
    st.download_button(
        label="📥 Stáhnout prodeje.csv (Excel-friendly)",
        data=csv_data,
        file_name="prodeje.csv",
        mime="text/csv",
        type="primary"
    )
except FileNotFoundError:
    st.error("Soubor data/prodeje.csv nebyl nalezen.")

st.divider()

# --- MOŽNOST 3: VEŘEJNÉ ZDROJE ---
st.header("3. Veřejné databáze")
st.markdown("Chcete analyzovat něco reálného, ale nemáte vlastní data? Zkuste tyto zdroje:")

c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("🌍 Světová data")
    st.markdown("**[Kaggle Datasets](https://www.kaggle.com/datasets)**")
    st.caption("Obrovská databáze všeho možného. Nutná registrace.")
    st.markdown("""
    *   [Titanic](https://www.kaggle.com/c/titanic/data)
    *   [Netflix Movies](https://www.kaggle.com/shivamb/netflix-shows)
    *   [Airbnb NYC](https://www.kaggle.com/dgomonov/new-york-city-airbnb-open-data)
    """)

with c2:
    st.subheader("🇨🇿 Česká data")
    st.markdown("**[Data.gov.cz](https://data.gov.cz/)**")
    st.caption("Oficiální otevřená data ČR.")
    st.markdown("""
    *   [Dopravní nehody](https://data.gov.cz/datová-sada?iri=https%3A%2F%2Fdata.gov.cz%2Fzdroj%2Fdatové-sady%2F00007064%2F853503930)
    *   [Volby](https://www.volby.cz/opendata/opendata.htm)
    *   [ČSÚ (Statistiky)](https://www.czso.cz/csu/czso/otevrena_data)
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
