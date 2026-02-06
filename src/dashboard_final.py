import streamlit as st
import pandas as pd
import altair as alt

# --- 1. Konfigurace stránky ---
st.set_page_config(
    page_title="Ceny PHM v ČR",
    page_icon="⛽",
    layout="wide"
)

# --- 2. Načtení a příprava dat ---
@st.cache_data
def load_data():
    df = pd.read_csv('data/CENPHMT.csv')
    df.rename(columns={'Hodnota': 'Cena', 'CASTPHM': 'Tydentext', 'Druh PHM': 'Produkt'}, inplace=True)
    df['Datum'] = pd.to_datetime(df['Tydentext'] + '-1', format='%Y-W%W-%w')
    return df

df = load_data()

# --- 3. Sidebar (Filtry) ---
st.sidebar.header("Filtry")

produkty = st.sidebar.multiselect(
    "Vyberte druh paliva:",
    options=df['Produkt'].unique(),
    default=df['Produkt'].unique()
)

df_filtered = df[df['Produkt'].isin(produkty)]

# --- 4. Hlavní obsah ---
st.title("⛽ Vývoj cen pohonných hmot v ČR")

if df_filtered.empty:
    st.warning("Vyberte alespoň jeden druh paliva.")
    st.stop()

# KPI
latest_date = df_filtered['Datum'].max()
latest_data = df_filtered[df_filtered['Datum'] == latest_date]

st.subheader(f"Ceny v posledním týdnu ({latest_date.strftime('%d. %m. %Y')})")
cols = st.columns(len(latest_data))
for i, row in enumerate(latest_data.itertuples()):
    cols[i].metric(row.Produkt, f"{row.Cena:.2f} Kč")

st.markdown("---")

# Graf vývoje v čase
st.subheader("Vývoj cen v čase")
chart_time = alt.Chart(df_filtered).mark_line().encode(
    x=alt.X('Datum:T', title='Datum'),
    y=alt.Y('Cena:Q', title='Cena (Kč/l)'),
    color='Produkt:N',
    tooltip=['Datum', 'Produkt', 'Cena']
).interactive()
st.altair_chart(chart_time, use_container_width=True)
