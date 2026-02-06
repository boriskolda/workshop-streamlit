import streamlit as st
import pandas as pd
import altair as alt
import datetime
import streamlit.components.v1 as components

# --- Konfigurace ---
st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('data/CENPHMT.csv')
    df.rename(columns={'Hodnota': 'Cena', 'CASTPHM': 'Tydentext', 'Druh PHM': 'Produkt'}, inplace=True)
    df['Datum'] = pd.to_datetime(df['Tydentext'] + '-1', format='%Y-W%W-%w')
    df = df[df['IndicatorType'] == '6621T'] # Filtr na průměrné ceny
    return df

df = load_data()

# --- Hlavní nadpis ---
st.title("🎛️ Interaktivita Masterclass: Ceny PHM")
st.caption("Nechte uživatele, ať si s daty hrají.")

# --- Navigace ---
tab_intro, tab_principle, tab_widgets, tab_filter, tab_state, tab_challenge = st.tabs([
    "🎬 PREZENTACE",
    "1. Princip", 
    "2. Katalog widgetů", 
    "3. Filtrování dat", 
    "4. Session State", 
    "🚀 KUCHAŘKA FILTRŮ"
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
    <title>Interactivity Masterclass</title>
    
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

        /* Individual Slide */
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
            transition: transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1), opacity 0.6s ease;
            opacity: 0;
            pointer-events: none;
            z-index: 0;
            transform: scale(0.95);
        }

        .slide.active {
            opacity: 1;
            pointer-events: auto;
            z-index: 20;
            transform: translateX(0) scale(1);
        }

        .slide.prev {
            opacity: 0;
            transform: translateX(-100%) scale(0.9);
            z-index: 10;
        }

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
            position: relative;
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
                        <div class="inline-block px-3 py-1 bg-purple-500/20 text-purple-300 rounded-full text-sm font-mono mb-6 border border-purple-500/30">
                            st.session_state
                        </div>
                        <h1>Interaktivita 🎛️<br><span class="text-purple-400">Aplikace, která žije</span></h1>
                        <p class="mt-6 text-xl">
                            Statický report je nuda. Uživatelé chtějí filtrovat, klikat a zkoumat. Streamlit dělá z interaktivity hračku.
                        </p>
                        <ul class="mt-8 space-y-4 text-slate-300">
                            <li class="flex items-center gap-3">
                                <i class="fas fa-sliders-h text-yellow-400"></i> Widgety jako proměnné
                            </li>
                            <li class="flex items-center gap-3">
                                <i class="fas fa-filter text-blue-400"></i> Okamžité filtrování dat
                            </li>
                            <li class="flex items-center gap-3">
                                <i class="fas fa-memory text-green-400"></i> Paměť aplikace (State)
                            </li>
                        </ul>
                    </div>
                    <div class="flex items-center justify-center">
                        <i class="fas fa-gamepad text-[15rem] text-purple-500/20 animate-pulse"></i>
                    </div>
                </div>
                <div class="card-footer p-6 border-t border-slate-700 bg-slate-800/50 flex justify-between text-slate-500 font-mono text-sm">
                    <span>user input -> action</span>
                    <span>Použij šipky ➝</span>
                </div>
            </div>
        </div>

        <!-- SLIDE 1: WIDGETY -->
        <div class="slide next" id="slide-1">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-slate-200 font-bold">1. Widget = Funkce</h3>
                    <i class="fas fa-calculator text-purple-400"></i>
                </div>
                <div class="card-body">
                    <div>
                        <div class="feature-icon bg-purple-500/20 text-purple-400"><i class="fas fa-equals"></i></div>
                        <h2>Všechno je návratová hodnota</h2>
                        <p>Zapomeňte na složité "Event Listenery" z JavaScriptu. Ve Streamlitu widget prostě <strong>vrátí hodnotu</strong>, kterou si uživatel vybral.</p>
                        <p>Když uživatel pohne sliderem, skript se spustí znovu a funkce vrátí nové číslo.</p>
                    </div>
                    <div class="code-window">
                        <div class="code-header">
                            <div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div>
                        </div>
                        <div class="code-content">
                            <span class="comment"># Uživatel vybere číslo</span><br>
                            vek = st.<span class="func">slider</span>(<span class="str">"Věk"</span>, <span class="num">0</span>, <span class="num">100</span>)<br><br>
                            <span class="comment"># Uživatel napíše text</span><br>
                            jmeno = st.<span class="func">text_input</span>(<span class="str">"Jméno"</span>)<br><br>
                            <span class="comment"># Hned to můžeme použít</span><br>
                            <span class="kwd">if</span> vek > <span class="num">18</span>:<br>
                            &nbsp;&nbsp;st.<span class="func">write</span>(f<span class="str">"Ahoj {jmeno}, dej si pivo!"</span>)
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 2: FILTROVÁNÍ -->
        <div class="slide next" id="slide-2">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-slate-200 font-bold">2. Propojení s Daty</h3>
                    <i class="fas fa-filter text-purple-400"></i>
                </div>
                <div class="card-body">
                    <div>
                        <div class="feature-icon bg-blue-500/20 text-blue-400"><i class="fas fa-link"></i></div>
                        <h2>Widget ovládá Pandas</h2>
                        <p>Tohle je nejčastější vzor (pattern) ve Streamlitu:</p>
                        <ol class="list-decimal list-inside space-y-2 text-slate-300 ml-2">
                            <li>Vytvoř widget (např. výběr města).</li>
                            <li>Ulož jeho hodnotu do proměnné.</li>
                            <li>Použij proměnnou k filtrování DataFrame.</li>
                            <li>Zobraz vyfiltrovaná data.</li>
                        </ol>
                    </div>
                    <div class="code-window">
                        <div class="code-header">
                            <div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div>
                        </div>
                        <div class="code-content">
                            <span class="comment"># 1. Widget</span><br>
                            mesto = st.<span class="func">selectbox</span>(<span class="str">"Vyber město"</span>, [<span class="str">"Praha"</span>, <span class="str">"Brno"</span>])<br><br>
                            <span class="comment"># 2. Filtr</span><br>
                            df_filtered = df[df[<span class="str">'Mesto'</span>] == mesto]<br><br>
                            <span class="comment"># 3. Zobrazení</span><br>
                            st.<span class="func">dataframe</span>(df_filtered)<br>
                            st.<span class="func">bar_chart</span>(df_filtered)
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 3: SESSION STATE -->
        <div class="slide next" id="slide-3">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-slate-200 font-bold">3. Session State (Paměť)</h3>
                    <i class="fas fa-brain text-purple-400"></i>
                </div>
                <div class="card-body">
                    <div>
                        <div class="feature-icon bg-orange-500/20 text-orange-400"><i class="fas fa-history"></i></div>
                        <h2>Problém Amnézie</h2>
                        <p>Protože se skript spouští pořád dokola, proměnné se při každém kliknutí "vynulují".</p>
                        <p>Pokud chcete, aby si aplikace něco pamatovala (např. obsah nákupního košíku nebo historii chatu), musíte použít <code>st.session_state</code>.</p>
                    </div>
                    <div class="code-window">
                        <div class="code-header">
                            <div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div>
                        </div>
                        <div class="code-content">
                            <span class="comment"># Inicializace (jen poprvé)</span><br>
                            <span class="kwd">if</span> <span class="str">'pocitadlo'</span> <span class="kwd">not in</span> st.session_state:<br>
                            &nbsp;&nbsp;st.session_state.pocitadlo = <span class="num">0</span><br><br>
                            <span class="comment"># Změna hodnoty</span><br>
                            <span class="kwd">if</span> st.<span class="func">button</span>(<span class="str">"Přičti 1"</span>):<br>
                            &nbsp;&nbsp;st.session_state.pocitadlo += <span class="num">1</span><br><br>
                            st.<span class="func">write</span>(st.session_state.pocitadlo)
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 4: CALLBACKS -->
        <div class="slide next" id="slide-4">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-slate-200 font-bold">4. Callbacks (Pokročilé)</h3>
                    <i class="fas fa-bolt text-purple-400"></i>
                </div>
                <div class="card-body">
                    <div>
                        <div class="feature-icon bg-green-500/20 text-green-400"><i class="fas fa-running"></i></div>
                        <h2>Akce při změně</h2>
                        <p>Někdy chcete spustit funkci PŘESNĚ v okamžiku, kdy uživatel klikne, ještě předtím, než se překreslí zbytek stránky.</p>
                        <p>K tomu slouží parametr <code>on_change</code> nebo <code>on_click</code>.</p>
                    </div>
                    <div class="code-window">
                        <div class="code-header">
                            <div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div>
                        </div>
                        <div class="code-content">
                            <span class="kwd">def</span> <span class="func">vycisti_formular</span>():<br>
                            &nbsp;&nbsp;st.session_state.text = <span class="str">""</span><br><br>
                            st.<span class="func">text_input</span>(<br>
                            &nbsp;&nbsp;<span class="str">"Napiš něco"</span>,<br>
                            &nbsp;&nbsp;key=<span class="str">"text"</span>,<br>
                            &nbsp;&nbsp;on_change=vycisti_formular<br>
                            )
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
            <button onclick="toggleFullscreen()" class="w-12 h-12 rounded-full bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center transition border border-slate-600 focus:outline-none focus:ring-2 focus:ring-purple-500 cursor-pointer" title="Fullscreen">
                <i class="fas fa-expand"></i>
            </button>
            <button onclick="prevSlide()" class="w-12 h-12 rounded-full bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center transition border border-slate-600 focus:outline-none cursor-pointer">
                <i class="fas fa-arrow-left"></i>
            </button>
            <button onclick="nextSlide()" class="w-12 h-12 rounded-full bg-purple-600 hover:bg-purple-500 text-white flex items-center justify-center transition shadow-lg shadow-purple-900/50 focus:outline-none cursor-pointer">
                <i class="fas fa-arrow-right"></i>
            </button>
        </div>
    </div>

    <!-- Progress Bar -->
    <div class="fixed top-0 left-0 h-1 bg-slate-800 w-full z-50">
        <div id="progress-bar" class="h-full bg-purple-500 transition-all duration-300" style="width: 20%"></div>
    </div>

    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        const progressBar = document.getElementById('progress-bar');
        const counter = document.getElementById('slide-counter');

        function updateSlide() {
            slides.forEach((slide, index) => {
                slide.className = 'slide';
                if (index === currentSlide) {
                    slide.classList.add('active');
                } else if (index < currentSlide) {
                    slide.classList.add('prev');
                } else {
                    slide.classList.add('next');
                }
            });

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

        updateSlide();
    </script>
</body>
</html>
    """
    components.html(html_code, height=850, scrolling=False)

# ==========================================
# TAB 1: PRINCIP
# ==========================================
with tab_principle:
    st.header("🔄 Jak fungují widgety?")
    st.markdown("""
    Ve Streamlitu je widget jen funkce, která **vrací hodnotu**.
    
    *   Když uživatel pohne posuvníkem, Streamlit spustí skript znovu.
    *   Funkce widgetu vrátí novou hodnotu.
    *   Tuto hodnotu uložíte do proměnné a použijete dál v kódu.
    """)
    
    st.code("""
# 1. Vytvoříme widget a uložíme výsledek do proměnné
jmeno = st.text_input("Jak se jmenuješ?")

# 2. Použijeme proměnnou
st.write(f"Ahoj {jmeno}!")
    """, language="python")
    
    st.divider()
    
    # Živá ukázka
    col1, col2 = st.columns(2)
    with col1:
        jmeno = st.text_input("Jak se jmenuješ?", key="demo_name")
    with col2:
        if jmeno:
            st.success(f"Ahoj **{jmeno}**! 👋")
        else:
            st.info("Napiš něco vlevo...")

# ==========================================
# TAB 2: KATALOG WIDGETŮ
# ==========================================
with tab_widgets:
    st.header("🎛️ Katalog widgetů")
    st.markdown("To nejlepší, co Streamlit nabízí.")

    # 1. Výběry
    st.subheader("1. Výběry (Selection)")
    c1, c2 = st.columns(2)
    with c1:
        st.code('st.selectbox("Vyber", ["A", "B"])', language="python")
        st.selectbox("Vyber jednu možnost", ["Možnost A", "Možnost B"], key="sb")
    with c2:
        st.code('st.multiselect("Vyber", ["A", "B"])', language="python")
        st.multiselect("Vyber více možností", ["A", "B", "C"], default=["A"], key="ms")

    st.divider()

    # 2. Čísla a Posuvníky
    st.subheader("2. Čísla a Posuvníky")
    c1, c2 = st.columns(2)
    with c1:
        st.code('st.slider("Věk", 0, 100, 25)', language="python")
        st.slider("Nastav věk", 0, 100, 25, key="sl")
    with c2:
        st.code('st.number_input("Cena", 0, 1000)', language="python")
        st.number_input("Zadej cenu", 0, 1000, 100, key="ni")

    st.divider()

    # 3. Datum a Čas
    st.subheader("3. Datum a Čas")
    c1, c2 = st.columns(2)
    with c1:
        st.code('st.date_input("Datum")', language="python")
        st.date_input("Kdy?", datetime.date.today(), key="di")
    with c2:
        st.code('st.time_input("Čas")', language="python")
        st.time_input("V kolik?", datetime.time(12, 00), key="ti")

    st.divider()

    # 4. Tlačítka
    st.subheader("4. Akce")
    c1, c2 = st.columns(2)
    with c1:
        st.code('st.button("Klikni")', language="python")
        if st.button("Klikni na mě", key="btn"):
            st.balloons()
    with c2:
        st.code('st.checkbox("Zobrazit")', language="python")
        st.checkbox("Zobrazit detaily", key="cb")

# ==========================================
# TAB 3: FILTROVÁNÍ DAT
# ==========================================
with tab_filter:
    st.header("🔍 Propojení s daty (Filtrování)")
    st.markdown("Tohle je svatý grál dashboardů. Widget ovládá Pandas filtr.")

    st.subheader("Krok 1: Widget")
    st.code("""
produkty = df['Produkt'].unique()
vyber = st.multiselect("Vyber produkt:", produkty, default=produkty[0:3])
    """, language="python")
    
    produkty = df['Produkt'].unique()
    vyber = st.multiselect("Vyber produkt:", produkty, default=list(produkty[0:3]), key="filter_demo")

    st.subheader("Krok 2: Filtrace DataFrame")
    st.code("""
# Magický řádek
filtered_df = df[df['Produkt'].isin(vyber)]
    """, language="python")
    
    filtered_df = df[df['Produkt'].isin(vyber)]

    st.subheader("Krok 3: Výsledek")
    st.dataframe(filtered_df, hide_index=True)

# ==========================================
# TAB 4: SESSION STATE
# ==========================================
with tab_state:
    st.header("🧠 Session State (Paměť)")
    st.markdown("""
    Streamlit při každém kliknutí "zapomene" proměnné, protože jede od začátku.
    Pokud si chcete něco pamatovat (např. nákupní košík), musíte použít `st.session_state`.
    """)

    st.code("""
if 'pocitadlo' not in st.session_state:
    st.session_state.pocitadlo = 0

if st.button("Přičti 1"):
    st.session_state.pocitadlo += 1

st.write(f"Hodnota: {st.session_state.pocitadlo}")
    """, language="python")

    # Demo
    if 'pocitadlo' not in st.session_state:
        st.session_state.pocitadlo = 0

    c1, c2 = st.columns([1, 4])
    with c1:
        if st.button("➕ Přičti 1", key="state_btn"):
            st.session_state.pocitadlo += 1
    with c2:
        st.metric("Počítadlo", st.session_state.pocitadlo)

# ==========================================
# TAB 5: KUCHAŘKA FILTRŮ
# ==========================================
with tab_challenge:
    st.header("🚀 Kuchařka filtrů")
    st.markdown("Vyberte si, jaký filtr chcete přidat do aplikace.")

    col1, col2 = st.columns([1, 2])

    with col1:
        filter_type = st.radio(
            "Vyberte typ filtru:",
            ["Výběr paliva (Multiselect)", "Výběr data (Date Input)"]
        )

    with col2:
        st.subheader("Kód a výsledek")
        
        if "Výběr paliva" in filter_type:
            st.info("Filtr pro výběr jednoho nebo více druhů paliva.")
            code = """
# 1. Získat unikátní hodnoty
moznosti = df['Produkt'].unique()

# 2. Vytvořit widget
vyber = st.sidebar.multiselect(
    "Vyber palivo:",
    options=moznosti,
    default=moznosti
)

# 3. Aplikovat filtr
df_filtered = df[df['Produkt'].isin(vyber)]
"""
            st.code(code, language="python")
            
        elif "Výběr data" in filter_type:
            st.info("Filtr pro výběr časového rozsahu.")
            code = """
# 1. Vytvořit widget
datum_od, datum_do = st.sidebar.date_input(
    "Vyber rozsah:",
    [df['Datum'].min(), df['Datum'].max()]
)

# 2. Aplikovat filtr
df_filtered = df[
    (df['Datum'] >= pd.to_datetime(datum_od)) &
    (df['Datum'] <= pd.to_datetime(datum_do))
]
"""
            st.code(code, language="python")
