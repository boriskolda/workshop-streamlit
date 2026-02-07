import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

# --- Konfigurace a Data ---
st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('data/CEN0101J.csv')
    df.rename(columns={'Hodnota': 'Cena', 'CasM': 'RokMesic', 'Druh PHM': 'Produkt'}, inplace=True)
    df['Datum'] = pd.to_datetime(df['RokMesic'], format='%Y-%M')
    return df

df = load_data()

# --- Hlavní nadpis ---
st.title("🐼 Pandas Masterclass: Ceny pohonných hmot")
st.caption("Analyzujeme reálná data o cenách paliv z ČSÚ.")

# --- Navigace ---
tab_intro, tab_load, tab_clean, tab_transform, tab_agg, tab_challenge = st.tabs([
    "🎬 PREZENTACE",
    "1. Načtení & Průzkum", 
    "2. Čištění dat", 
    "3. Transformace", 
    "4. Agregace", 
    "🚀 PŘÍPRAVA PRO GRAFY"
])

# ==========================================
# TAB 0: PREZENTACE
# ==========================================
with tab_intro:
    html_code = """
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pandas Power Demo</title>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">

    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0f172a; /* Slate 900 */
            color: #f1f5f9;
            overflow: hidden;
            margin: 0;
        }

        /* Slide Container */
        .slide-container {
            position: relative;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
        }

        /* Individual Slide Logic - ROBUST FIX */
        .slide {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            
            /* Smooth Transition */
            transition: transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1), opacity 0.6s ease;
            
            /* Default Hidden State */
            opacity: 0;
            pointer-events: none;
            z-index: 0;
            transform: scale(0.95);
        }

        /* Active Slide */
        .slide.active {
            opacity: 1;
            pointer-events: auto;
            z-index: 20;
            transform: translateX(0) scale(1);
        }

        /* Previous Slide (Exit Left) */
        .slide.prev {
            opacity: 0;
            transform: translateX(-100%) scale(0.9);
            z-index: 10;
        }

        /* Next Slide (Waiting Right) */
        .slide.next {
            opacity: 0;
            transform: translateX(100%) scale(0.9);
            z-index: 10;
        }

        /* Content Card */
        .card {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 1.5rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            width: 100%;
            max-width: 1280px;
            min-height: 650px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            position: relative; /* Ensure z-index works inside */
        }

        .card-header {
            padding: 2rem 3rem;
            border-bottom: 1px solid #334155;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(30, 41, 59, 0.95);
        }

        .card-body {
            padding: 3rem;
            flex-grow: 1;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            align-items: center;
        }

        /* Code Window Styling */
        .code-window {
            background: #0d1117;
            border-radius: 0.75rem;
            border: 1px solid #30363d;
            overflow: hidden;
            font-family: 'JetBrains Mono', monospace;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        }

        .code-header {
            background: #161b22;
            padding: 0.75rem 1rem;
            display: flex;
            gap: 0.5rem;
            border-bottom: 1px solid #30363d;
        }

        .dot { width: 0.75rem; height: 0.75rem; border-radius: 50%; }
        .dot-red { background: #ff5f56; }
        .dot-yellow { background: #ffbd2e; }
        .dot-green { background: #27c93f; }

        .code-content {
            padding: 1.5rem;
            color: #c9d1d9;
            font-size: 1rem;
            line-height: 1.6;
        }

        /* Syntax Highlighting */
        .kwd { color: #ff7b72; } 
        .str { color: #a5d6ff; } 
        .func { color: #d2a8ff; } 
        .var { color: #79c0ff; } 
        .comment { color: #8b949e; font-style: italic; } 
        .num { color: #79c0ff; } 

        /* Typography */
        h1 { font-size: 3rem; font-weight: 800; color: #fff; line-height: 1.1; }
        h2 { font-size: 2.25rem; font-weight: 700; color: #fff; margin-bottom: 1rem; }
        p { color: #94a3b8; font-size: 1.125rem; line-height: 1.6; margin-bottom: 1.5rem; }
        
        .feature-icon {
            width: 3rem;
            height: 3rem;
            border-radius: 0.75rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
        }
    </style>
</head>
<body>

    <div class="slide-container">

        <!-- SLIDE 0: INTRO -->
        <div class="slide active" id="slide-0">
            <div class="card">
                <div class="card-body" style="grid-template-columns: 1.2fr 0.8fr;">
                    <div>
                        <div class="inline-block px-3 py-1 bg-indigo-500/20 text-indigo-300 rounded-full text-sm font-mono mb-6 border border-indigo-500/30">
                            import pandas as pd
                        </div>
                        <h1>Síla Pandas 🐼<br><span class="text-indigo-400">Excel na steroidech</span></h1>
                        <p class="mt-6 text-xl">
                            Pandas je standard pro analýzu dat v Pythonu. Umožňuje načítat, čistit, transformovat a analyzovat miliony řádků dat během zlomku vteřiny.
                        </p>
                        <ul class="mt-8 space-y-4 text-slate-300">
                            <li class="flex items-center gap-3">
                                <i class="fas fa-bolt text-yellow-400"></i> 100x rychlejší než manuální práce
                            </li>
                            <li class="flex items-center gap-3">
                                <i class="fas fa-database text-blue-400"></i> Načte cokoliv (CSV, Excel, SQL)
                            </li>
                            <li class="flex items-center gap-3">
                                <i class="fas fa-code text-green-400"></i> Automatizovatelné skripty
                            </li>
                        </ul>
                    </div>
                    <div class="flex items-center justify-center">
                        <i class="fas fa-table text-[15rem] text-indigo-500/20 animate-pulse"></i>
                    </div>
                </div>
                <div class="card-footer p-6 border-t border-slate-700 bg-slate-800/50 flex justify-between text-slate-500 font-mono text-sm">
                    <span>pandas 2.0+</span>
                    <span>Použij šipky ➝</span>
                </div>
            </div>
        </div>

        <!-- SLIDE 1: NAČÍTÁNÍ -->
        <div class="slide next" id="slide-1">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-slate-200 font-bold">1. Načtení dat</h3>
                    <i class="fas fa-file-import text-indigo-400"></i>
                </div>
                <div class="card-body">
                    <div>
                        <div class="feature-icon bg-blue-500/20 text-blue-400"><i class="fas fa-file-csv"></i></div>
                        <h2>Vše začíná daty</h2>
                        <p>Zapomeňte na `Otevřít soubor > Importovat > Nastavit oddělovač`. Pandas automaticky detekuje formáty a načte data do struktury zvané <strong>DataFrame</strong>.</p>
                        <p>DataFrame je jako tabulka v Excelu, ale žije v paměti RAM a je připravena na programování.</p>
                    </div>
                    <div class="code-window">
                        <div class="code-header">
                            <div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div>
                        </div>
                        <div class="code-content">
                            <span class="kwd">import</span> pandas <span class="kwd">as</span> pd<br><br>
                            <span class="comment"># Načtení z CSV</span><br>
                            df = pd.<span class="func">read_csv</span>(<span class="str">"prodeje_2024.csv"</span>)<br><br>
                            <span class="comment"># Načtení z Excelu</span><br>
                            df_xl = pd.<span class="func">read_excel</span>(<span class="str">"report.xlsx"</span>)<br><br>
                            <span class="comment"># Rychlý náhled prvních 5 řádků</span><br>
                            <span class="func">print</span>(df.<span class="func">head</span>())
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 2: FILTROVÁNÍ -->
        <div class="slide next" id="slide-2">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-slate-200 font-bold">2. Průzkum a Filtrování</h3>
                    <i class="fas fa-filter text-indigo-400"></i>
                </div>
                <div class="card-body">
                    <div>
                        <div class="feature-icon bg-green-500/20 text-green-400"><i class="fas fa-search"></i></div>
                        <h2>Žádné "For" cykly</h2>
                        <p>V Pythonu běžně používáme cykly. V Pandas <strong>NE</strong>. Používáme tzv. <em>vektorizované operace</em>.</p>
                        <p>Chcete vyfiltrovat data? Stačí napsat podmínku přímo do závorek. Je to čitelné (skoro jako angličtina) a extrémně rychlé.</p>
                    </div>
                    <div class="code-window">
                        <div class="code-header">
                            <div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div>
                        </div>
                        <div class="code-content">
                            <span class="comment"># Zjistit základní statistiky (průměr, max, min)</span><br>
                            stats = df.<span class="func">describe</span>()<br><br>
                            <span class="comment"># FILTROVÁNÍ:</span><br>
                            <span class="comment"># Vyber objednávky nad 1000 Kč</span><br>
                            velke_objednavky = df[df[<span class="str">'cena'</span>] > <span class="num">1000</span>]<br><br>
                            <span class="comment"># Kombinace podmínek (Brno A nad 1000)</span><br>
                            brno_vip = df[(df[<span class="str">'mesto'</span>] == <span class="str">'Brno'</span>) & (df[<span class="str">'cena'</span>] > <span class="num">1000</span>)]
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 3: AGREGACE -->
        <div class="slide next" id="slide-3">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-slate-200 font-bold">3. Agregace (GroupBy)</h3>
                    <i class="fas fa-layer-group text-indigo-400"></i>
                </div>
                <div class="card-body">
                    <div>
                        <div class="feature-icon bg-purple-500/20 text-purple-400"><i class="fas fa-calculator"></i></div>
                        <h2>Pivot Table v kódu</h2>
                        <p>Metoda <code>.groupby()</code> je magie. Rozdělí data do skupin, aplikuje funkci (suma, průměr) a složí je zpět.</p>
                        <p>Odpovědi na otázky typu <em>"Kolik jsme prodali v každém městě?"</em> nebo <em>"Jaká je průměrná cena podle kategorie?"</em> získáte na jeden řádek.</p>
                    </div>
                    <div class="code-window">
                        <div class="code-header">
                            <div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div>
                        </div>
                        <div class="code-content">
                            <span class="comment"># Celkové tržby podle města</span><br>
                            trzby_mesta = df.<span class="func">groupby</span>(<span class="str">'mesto'</span>)[<span class="str">'cena'</span>].<span class="func">sum</span>()<br><br>
                            <span class="comment"># Průměrný věk zákazníků podle pohlaví</span><br>
                            vek_demo = df.<span class="func">groupby</span>(<span class="str">'pohlavi'</span>)[<span class="str">'vek'</span>].<span class="func">mean</span>()<br><br>
                            <span class="comment"># Více agregací najednou</span><br>
                            report = df.<span class="func">groupby</span>(<span class="str">'kategorie'</span>).<span class="func">agg</span>({<br>
                            &nbsp;&nbsp;<span class="str">'cena'</span>: [<span class="str">'sum'</span>, <span class="str">'mean'</span>],<br>
                            &nbsp;&nbsp;<span class="str">'id'</span>: <span class="str">'count'</span><br>
                            })
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 4: ČIŠTĚNÍ DAT -->
        <div class="slide next" id="slide-4">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-slate-200 font-bold">4. Čištění a Čas</h3>
                    <i class="fas fa-broom text-indigo-400"></i>
                </div>
                <div class="card-body">
                    <div>
                        <div class="feature-icon bg-orange-500/20 text-orange-400"><i class="far fa-calendar-alt"></i></div>
                        <h2>Realita není dokonalá</h2>
                        <p>Data často obsahují chyby nebo prázdná místa. Pandas má vestavěné nástroje na jejich opravu.</p>
                        <p>Navíc exceluje v práci s časem. Chcete sečíst tržby po měsících? Metoda <code>resample</code> to udělá okamžitě.</p>
                    </div>
                    <div class="code-window">
                        <div class="code-header">
                            <div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div>
                        </div>
                        <div class="code-content">
                            <span class="comment"># Vyhození řádků, kde chybí data</span><br>
                            df_clean = df.<span class="func">dropna</span>()<br><br>
                            <span class="comment"># Vyplnění chybějících hodnot nulou</span><br>
                            df_filled = df.<span class="func">fillna</span>(<span class="num">0</span>)<br><br>
                            <span class="comment"># --- TIME SERIES MAGIC ---</span><br>
                            <span class="comment"># Převod textu na datum</span><br>
                            df[<span class="str">'datum'</span>] = pd.<span class="func">to_datetime</span>(df[<span class="str">'datum'</span>])<br><br>
                            <span class="comment"># Sečíst prodeje po měsících (M = Month)</span><br>
                            mesicni_prodeje = df.<span class="func">resample</span>(<span class="str">'M'</span>, on=<span class="str">'datum'</span>).<span class="func">sum</span>()
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <!-- CONTROLS -->
    <div class="fixed bottom-0 left-0 w-full p-6 flex justify-between items-center z-50 pointer-events-none">
        <div class="pointer-events-auto bg-slate-800/80 backdrop-blur px-4 py-2 rounded-full text-slate-400 font-mono text-sm border border-slate-700">
            <span id="slide-counter">1 / 5</span>
        </div>
        
        <div class="pointer-events-auto flex gap-4">
            <button onclick="toggleFullscreen()" class="w-12 h-12 rounded-full bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center transition border border-slate-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer" title="Fullscreen">
                <i class="fas fa-expand"></i>
            </button>
            <button onclick="prevSlide()" class="w-12 h-12 rounded-full bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center transition border border-slate-600 focus:outline-none cursor-pointer">
                <i class="fas fa-arrow-left"></i>
            </button>
            <button onclick="nextSlide()" class="w-12 h-12 rounded-full bg-indigo-600 hover:bg-indigo-500 text-white flex items-center justify-center transition shadow-lg shadow-indigo-900/50 focus:outline-none cursor-pointer">
                <i class="fas fa-arrow-right"></i>
            </button>
        </div>
    </div>

    <!-- Progress Bar -->
    <div class="fixed top-0 left-0 h-1 bg-slate-800 w-full z-50">
        <div id="progress-bar" class="h-full bg-indigo-500 transition-all duration-300" style="width: 20%"></div>
    </div>

    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        const progressBar = document.getElementById('progress-bar');
        const counter = document.getElementById('slide-counter');

        function updateSlide() {
            slides.forEach((slide, index) => {
                // Hard reset of classes to prevent sticking
                slide.className = 'slide';
                
                if (index === currentSlide) {
                    slide.classList.add('active');
                } else if (index < currentSlide) {
                    slide.classList.add('prev');
                } else {
                    slide.classList.add('next');
                }
            });

            // Update Progress
            const progress = ((currentSlide + 1) / totalSlides) * 100;
            progressBar.style.width = `${progress}%`;
            counter.innerText = `${currentSlide + 1} / ${totalSlides}`;
        }

        function nextSlide() {
            if (currentSlide < totalSlides - 1) {
                currentSlide++;
                updateSlide();
            }
        }

        function prevSlide() {
            if (currentSlide > 0) {
                currentSlide--;
                updateSlide();
            }
        }
        
        function toggleFullscreen() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch(err => {
                    alert(`Error attempting to enable fullscreen: ${err.message}`);
                });
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                }
            }
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
            if (e.key === 'ArrowLeft') prevSlide();
            if (e.key === 'f') toggleFullscreen();
        });

        // Init
        updateSlide();
    </script>
</body>
</html>
    """
    components.html(html_code, height=850, scrolling=False)

# ==========================================
# TAB 1: NAČTENÍ A PRŮZKUM
# ==========================================
with tab_load:
    st.header("🔍 Průzkum dat: Ceny PHM")
    st.code("df = pd.read_csv('data/CEN0101J.csv')", language="python")
    st.dataframe(df.head())
    st.text(f"Počet řádků: {df.shape[0]}, Počet sloupců: {df.shape[1]}")

    st.divider()
    st.subheader("Další užitečné metody pro průzkum")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**1. Informace o datech**")
        st.code("""
# Zobrazí datové typy a počet neprázdných hodnot
df.info()

# Základní statistiky (průměr, min, max, kvartily)
df.describe()
        """, language="python")

        st.markdown("**2. Výběr sloupců**")
        st.code("""
# Výběr jednoho sloupce
df['Produkt']

# Výběr více sloupců
df[['Produkt', 'Cena']]
        """, language="python")

    with col2:
        st.markdown("**3. Unikátní hodnoty**")
        st.code("""
# Zobrazí unikátní hodnoty ve sloupci
df['Produkt'].unique()

# Počet unikátních hodnot
df['Produkt'].nunique()
        """, language="python")
        
        st.markdown("**4. Třídění**")
        st.code("""
# Seřazení podle ceny (vzestupně)
df.sort_values('Cena')

# Seřazení sestupně
df.sort_values('Cena', ascending=False)
        """, language="python")

# ==========================================
# TAB 2: ČIŠTĚNÍ DAT
# ==========================================
with tab_clean:
    st.header("🧹 Čištění dat")
    st.markdown("Přejmenování sloupců a převod na správné datové typy.")
    st.code("""
df.rename(columns={'Hodnota': 'Cena', 'CASTPHM': 'Tydentext', 'Druh PHM': 'Produkt'}, inplace=True)
# Převod textového týdne (např. '2016-W01') na skutečné datum
df['Datum'] = pd.to_datetime(df['RokMesic'], format='%Y-%M')
    """, language="python")
    st.dataframe(df[['Datum', 'Produkt', 'Cena']].head())

    st.divider()
    st.subheader("Další užitečné metody")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**1. Chybějící hodnoty**")
        st.code("""
# Odstranění řádků s chybějícími daty
df_clean = df.dropna()

# Nahrazení chybějících hodnot (např. nulou)
df_filled = df.fillna(0)
        """, language="python")

        st.markdown("**2. Duplicity**")
        st.code("""
# Odstranění duplicitních řádků
df_unique = df.drop_duplicates()
        """, language="python")

    with col2:
        st.markdown("**3. Změna datových typů**")
        st.code("""
# Převod sloupce na text
df['Produkt'] = df['Produkt'].astype(str)

# Převod na číslo (pokud to jde)
df['Cena'] = pd.to_numeric(df['Cena'], errors='coerce')
        """, language="python")
        
        st.markdown("**4. Práce s textem**")
        st.code("""
# Oříznutí mezer
df['Produkt'] = df['Produkt'].str.strip()

# Převod na malá písmena
df['Produkt'] = df['Produkt'].str.lower()
        """, language="python")

# ==========================================
# TAB 3: TRANSFORMACE
# ==========================================
with tab_transform:
    st.header("🛠️ Feature Engineering")
    st.markdown("Vytvoření sloupce 'Rok' a 'Měsíc'.")
    df['Rok'] = df['Datum'].dt.year
    df['Mesic'] = df['Datum'].dt.month
    st.code("""
df['Rok'] = df['Datum'].dt.year
df['Mesic'] = df['Datum'].dt.month
    """, language="python")
    st.dataframe(df[['Datum', 'Rok', 'Mesic']].head())

    st.divider()
    st.subheader("Další užitečné metody")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**1. Matematické operace**")
        st.code("""
# Vytvoření nového sloupce výpočtem
df['Cena_s_DPH'] = df['Cena'] * 1.21

# Rozdíl dvou sloupců
df['Zisk'] = df['Prodej'] - df['Naklady']
        """, language="python")

        st.markdown("**2. Podmínky (np.where)**")
        st.code("""
# Pokud je cena > 40, napiš 'Drahé', jinak 'Levné'
import numpy as np
df['Status'] = np.where(df['Cena'] > 40, 'Drahé', 'Levné')
        """, language="python")

    with col2:
        st.markdown("**3. Vlastní funkce (apply)**")
        st.code("""
# Aplikace funkce na každý řádek
def kategorizuj(x):
    return "Super" if x > 100 else "Normál"

df['Kategorie'] = df['Cena'].apply(kategorizuj)
        """, language="python")

        st.markdown("**4. Intervaly (cut)**")
        st.code("""
# Rozdělení do intervalů (binning)
df['Cenova_skupina'] = pd.cut(df['Cena'], bins=3, labels=['Nízká', 'Střední', 'Vysoká'])
        """, language="python")

# ==========================================
# TAB 4: AGREGACE
# ==========================================
with tab_agg:
    st.header("📊 Agregace")
    st.markdown("Průměrná cena podle 'Produktu' (druhu paliva).")
    st.code("df.groupby('Produkt')['Cena'].mean()", language="python")
    st.dataframe(df.groupby('Produkt')['Cena'].mean())

    st.divider()
    st.subheader("Další užitečné metody")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**1. Více funkcí najednou**")
        st.code("""
# Průměr a součet pro každou skupinu
df.groupby('Produkt')['Cena'].agg(['mean', 'sum', 'count'])
        """, language="python")

        st.markdown("**2. Seskupení podle více sloupců**")
        st.code("""
# Průměrná cena podle Produktu a Roku
df.groupby(['Produkt', 'Rok'])['Cena'].mean()
        """, language="python")

    with col2:
        st.markdown("**3. Pojmenovaná agregace**")
        st.code("""
# Vlastní názvy výsledných sloupců
df.groupby('Produkt').agg(
    Prumerna_cena=('Cena', 'mean'),
    Pocet_zaznamu=('Cena', 'count')
)
        """, language="python")

        st.markdown("**4. Reshaping (Pivot)**")
        st.code("""
# Pivot Table (s agregací - když jsou duplicity)
df.pivot_table(index='Rok', columns='Produkt', values='Cena', aggfunc='mean')

# Pivot (prosté přeskládání - pro unikátní kombinace)
# df.pivot(index='Datum', columns='Produkt', values='Cena')
        """, language="python")

# ==========================================
# TAB 5: PŘÍPRAVA PRO GRAFY
# ==========================================
with tab_challenge:
    st.header("🚀 Kuchařka: Příprava dat pro vizualizaci")
    st.markdown("Naklikejte si, jaké kroky potřebujete pro přípravu dat, a vygenerujte si kód.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Stavební bloky")
        
        show_imports = st.checkbox("1. Import knihovny", value=True, key="pd_imp_final")
        show_load = st.checkbox("2. Načtení a čištění dat", value=True, key="pd_load_final")
        
        st.markdown("---")
        
        pohled = st.radio(
            "Vyberte finální datový pohled:",
            ["Žádný", "Vývoj v čase", "Žebříček", "Jedno číslo (KPI)"],
            key="pd_pohled"
        )

    with col2:
        st.subheader("Výsledný kód a náhled")
        
        code_parts = []
        
        if show_imports:
            code_parts.append('''
# --- 1. IMPORT ---
import pandas as pd
''')
        
        if show_load:
            code_parts.append('''
# --- 2. NAČTENÍ A ZÁKLADNÍ ČIŠTĚNÍ ---
@st.cache_data
def priprav_data():
    df = pd.read_csv('data/CEN0101J.csv')
    df.rename(columns={'Hodnota': 'Cena', 'CASTPHM': 'Tydentext', 'Druh PHM': 'Produkt'}, inplace=True)
    df['Datum'] = pd.to_datetime(df['RokMesic'], format='%Y-%M')
    return df

df = priprav_data()
''')
        
        final_code = "".join(code_parts)
        
        # Vytvoření df_live pro náhledy
        df_live = pd.DataFrame()
        if show_load:
            df_live = load_data() # Použijeme již existující funkci load_data

        if "Vývoj v čase" in pohled:
            code = "df_v_case = df.groupby(['Datum', 'Produkt'])['Cena'].mean().reset_index()"
            final_code += f"\\n# --- POHLED: VÝVOJ V ČASE ---\\n{code}"
            st.code(final_code, language="python")
            if not df_live.empty:
                st.dataframe(df_live.groupby(['Datum', 'Produkt'])['Cena'].mean().reset_index().head(), hide_index=True)
            else:
                st.info("Načtěte data pro zobrazení náhledu.")

        elif "Žebříček" in pohled:
            code = "df_zebricek = df.groupby('Produkt')['Cena'].mean().sort_values(ascending=False).reset_index()"
            final_code += f"\\n# --- POHLED: ŽEBŘÍČEK ---\\n{code}"
            st.code(final_code, language="python")
            if not df_live.empty:
                st.dataframe(df_live.groupby('Produkt')['Cena'].mean().sort_values(ascending=False).reset_index().head(), hide_index=True)
            else:
                st.info("Načtěte data pro zobrazení náhledu.")

        elif "Jedno číslo (KPI)" in pohled:
            code = "prumerna_cena = df['Cena'].mean()"
            final_code += f"\\n# --- POHLED: JEDNO ČÍSLO (KPI) ---\\n{code}"
            st.code(final_code, language="python")
            if not df_live.empty:
                st.metric("Průměrná cena za celé období", f"{df_live['Cena'].mean():.2f} Kč")
            else:
                st.info("Načtěte data pro zobrazení náhledu.")
            
        else: # "Žádný"
            st.code(final_code, language="python")
            st.info("Vyberte si datový pohled vlevo pro zobrazení kódu a náhledu.")