import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import streamlit.components.v1 as components

# --- Konfigurace ---
st.set_page_config(layout="wide")

# --- Hlavní nadpis ---
st.title("👑 Streamlit Masterclass")
st.caption("Od prázdného skriptu k webové aplikaci za pár minut.")

# --- Navigace ---
tab_intro, tab_principle, tab_text, tab_layout, tab_data, tab_challenge = st.tabs([
    "🎬 PREZENTACE",
    "1. Princip fungování", 
    "2. Texty a Prvky", 
    "3. Layout (Rozložení)", 
    "4. Data a Grafy", 
    "🚀 STAVBA DASHBOARDU"
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
    <title>Streamlit Architecture Demo</title>
    
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
                        <div class="inline-block px-3 py-1 bg-red-500/20 text-red-300 rounded-full text-sm font-mono mb-6 border border-red-500/30">
                            import streamlit as st
                        </div>
                        <h1>Streamlit 👑<br><span class="text-red-400">Web bez HTML</span></h1>
                        <p class="mt-6 text-xl">
                            Streamlit je nejrychlejší způsob, jak vytvořit a sdílet datové aplikace. Promění obyčejný Python skript v interaktivní webovou stránku.
                        </p>
                        <ul class="mt-8 space-y-4 text-slate-300">
                            <li class="flex items-center gap-3">
                                <i class="fas fa-code text-yellow-400"></i> Jen čistý Python
                            </li>
                            <li class="flex items-center gap-3">
                                <i class="fas fa-sync-alt text-blue-400"></i> Okamžitý reload
                            </li>
                            <li class="flex items-center gap-3">
                                <i class="fas fa-cloud-upload-alt text-green-400"></i> Deployment na jedno kliknutí
                            </li>
                        </ul>
                    </div>
                    <div class="flex items-center justify-center">
                        <i class="fas fa-laptop-code text-[15rem] text-red-500/20 animate-pulse"></i>
                    </div>
                </div>
                <div class="card-footer p-6 border-t border-slate-700 bg-slate-800/50 flex justify-between text-slate-500 font-mono text-sm">
                    <span>streamlit run app.py</span>
                    <span>Použij šipky ➝</span>
                </div>
            </div>
        </div>

        <!-- SLIDE 1: DATA FLOW -->
        <div class="slide next" id="slide-1">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-slate-200 font-bold">1. Data Flow (Tok dat)</h3>
                    <i class="fas fa-water text-red-400"></i>
                </div>
                <div class="card-body">
                    <div>
                        <div class="feature-icon bg-red-500/20 text-red-400"><i class="fas fa-arrow-down"></i></div>
                        <h2>Shora dolů</h2>
                        <p>Streamlit čte váš kód jako knihu – od prvního řádku k poslednímu.</p>
                        <p>Kdykoliv se něco změní (uživatel klikne na tlačítko), Streamlit spustí <strong>celý skript znovu</strong> od začátku. To zní neefektivně, ale díky tomu je vývoj extrémně jednoduchý.</p>
                    </div>
                    <div class="flex flex-col items-center gap-4">
                        <div class="w-full p-4 bg-slate-800 border border-slate-600 rounded text-center">1. Načíst data</div>
                        <i class="fas fa-arrow-down text-slate-500"></i>
                        <div class="w-full p-4 bg-slate-800 border border-slate-600 rounded text-center">2. Vykreslit graf</div>
                        <i class="fas fa-arrow-down text-slate-500"></i>
                        <div class="w-full p-4 bg-red-900/30 border border-red-500 text-red-300 rounded text-center font-bold">3. Čekat na akci</div>
                        <div class="text-sm text-slate-500 mt-2">(Při akci -> Zpět na krok 1)</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 2: WIDGETY -->
        <div class="slide next" id="slide-2">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-slate-200 font-bold">2. Widgety jako Proměnné</h3>
                    <i class="fas fa-sliders-h text-red-400"></i>
                </div>
                <div class="card-body">
                    <div>
                        <div class="feature-icon bg-blue-500/20 text-blue-400"><i class="fas fa-keyboard"></i></div>
                        <h2>Žádné callbacky</h2>
                        <p>V jiných frameworcích musíte psát funkce, které "poslouchají" kliknutí. Ve Streamlitu widget prostě <strong>vrátí hodnotu</strong>.</p>
                        <p>Když uživatel pohne posuvníkem, skript se restartuje a funkce `st.slider()` vrátí nové číslo.</p>
                    </div>
                    <div class="code-window">
                        <div class="code-header">
                            <div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div>
                        </div>
                        <div class="code-content">
                            <span class="comment"># Vytvoří posuvník a uloží hodnotu</span><br>
                            vek = st.<span class="func">slider</span>(<span class="str">"Kolik ti je?"</span>, <span class="num">0</span>, <span class="num">100</span>)<br><br>
                            <span class="comment"># Použije hodnotu hned na dalším řádku</span><br>
                            st.<span class="func">write</span>(f<span class="str">"Je ti {vek} let."</span>)
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 3: CACHING -->
        <div class="slide next" id="slide-3">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-slate-200 font-bold">3. Caching (Paměť)</h3>
                    <i class="fas fa-memory text-red-400"></i>
                </div>
                <div class="card-body">
                    <div>
                        <div class="feature-icon bg-purple-500/20 text-purple-400"><i class="fas fa-bolt"></i></div>
                        <h2>Nenačítejte data pořád dokola</h2>
                        <p>Protože se skript spouští znovu a znovu, nechceme pokaždé stahovat 1GB soubor.</p>
                        <p>Dekorátor <code>@st.cache_data</code> řekne Streamlitu: <em>"Tuhle funkci spusť jen jednou a výsledek si zapamatuj."</em></p>
                    </div>
                    <div class="code-window">
                        <div class="code-header">
                            <div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div>
                        </div>
                        <div class="code-content">
                            <span class="kwd">@st.cache_data</span><br>
                            <span class="kwd">def</span> <span class="func">load_data</span>():<br>
                            &nbsp;&nbsp;<span class="comment"># Tohle se stane jen poprvé</span><br>
                            &nbsp;&nbsp;df = pd.<span class="func">read_csv</span>(<span class="str">"velky_soubor.csv"</span>)<br>
                            &nbsp;&nbsp;<span class="kwd">return</span> df<br><br>
                            <span class="comment"># Při rerunu se data vezmou z cache (bleskově)</span><br>
                            df = load_data()
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 4: LAYOUT -->
        <div class="slide next" id="slide-4">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-slate-200 font-bold">4. Layout</h3>
                    <i class="fas fa-th-large text-red-400"></i>
                </div>
                <div class="card-body">
                    <div>
                        <div class="feature-icon bg-green-500/20 text-green-400"><i class="fas fa-columns"></i></div>
                        <h2>Uspořádání stránky</h2>
                        <p>Streamlit není jen jedna dlouhá nudle. Můžete používat sloupce, záložky, postranní panel (sidebar) a expandery.</p>
                        <p>Vše se ovládá pomocí kontextových manažerů <code>with</code>.</p>
                    </div>
                    <div class="grid grid-cols-2 gap-4 text-center text-sm font-mono">
                        <div class="p-4 bg-slate-800 border border-slate-700 rounded">
                            st.sidebar
                        </div>
                        <div class="p-4 bg-slate-800 border border-slate-700 rounded">
                            st.columns([1, 2])
                        </div>
                        <div class="p-4 bg-slate-800 border border-slate-700 rounded">
                            st.tabs(["A", "B"])
                        </div>
                        <div class="p-4 bg-slate-800 border border-slate-700 rounded">
                            st.expander("Info")
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
            <button onclick="toggleFullscreen()" class="w-12 h-12 rounded-full bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center transition border border-slate-600 focus:outline-none focus:ring-2 focus:ring-red-500 cursor-pointer" title="Fullscreen">
                <i class="fas fa-expand"></i>
            </button>
            <button onclick="prevSlide()" class="w-12 h-12 rounded-full bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center transition border border-slate-600 focus:outline-none cursor-pointer">
                <i class="fas fa-arrow-left"></i>
            </button>
            <button onclick="nextSlide()" class="w-12 h-12 rounded-full bg-red-600 hover:bg-red-500 text-white flex items-center justify-center transition shadow-lg shadow-red-900/50 focus:outline-none cursor-pointer">
                <i class="fas fa-arrow-right"></i>
            </button>
        </div>
    </div>

    <!-- Progress Bar -->
    <div class="fixed top-0 left-0 h-1 bg-slate-800 w-full z-50">
        <div id="progress-bar" class="h-full bg-red-500 transition-all duration-300" style="width: 20%"></div>
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
    st.header("🔄 Jak to funguje?")
    st.markdown("""
    Streamlit je jiný než klasické webové frameworky (Django, Flask).
    
    1.  **Je to jen Python skript:** Píšete kód shora dolů.
    2.  **Magický Rerun:** Kdykoliv se něco změní (kliknete na tlačítko), **celý skript se spustí znovu od začátku**.
    3.  **Žádné HTML/CSS:** Všechny vizuální prvky jsou Python funkce.
    """)
    
    st.info("💡 **Tip:** Protože se skript spouští pořád dokola, musíme si dávat pozor na výkon (viz `@st.cache_data` později).")

    st.divider()
    
    st.subheader("Minimální aplikace")
    st.code("""
import streamlit as st

st.title("Ahoj světe!")
st.write("Tohle je moje první aplikace.")
    """, language="python")

# ==========================================
# TAB 2: TEXTY A PRVKY
# ==========================================
with tab_text:
    st.header("📝 Texty a Základní prvky")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Nadpisy")
        st.code("""
st.title("Hlavní nadpis")
st.header("Nadpis sekce")
st.subheader("Podnadpis")
        """, language="python")
        st.title("Hlavní nadpis")
        st.header("Nadpis sekce")
        st.subheader("Podnadpis")

    with col2:
        st.subheader("Formátování")
        st.code("""
st.write("Obyčejný text")
st.markdown("**Tučně**, *kurzíva*, [odkaz](...)")
st.info("Informační box")
st.success("Úspěch!")
st.error("Chyba!")
        """, language="python")
        st.write("Obyčejný text")
        st.markdown("**Tučně**, *kurzíva*")
        st.info("Informační box")
        st.success("Úspěch!")
        st.error("Chyba!")

    st.divider()
    
    st.subheader("📊 Klíčové ukazatele (Metriky)")
    st.markdown("`st.metric` je ideální pro zobrazení nejdůležitějších čísel (KPI) na první pohled. Manažeři to milují!")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.code('st.metric("Tržby", "1M", "+10%")', language="python")
        st.metric("Tržby", "1 000 000 Kč", "+10%")
    with c2:
        st.code('st.metric("Teplota", "24°C", "-2°C")', language="python")
        st.metric("Teplota", "24 °C", "-2 °C")
    with c3:
        st.code('st.metric("Status", "OK")', language="python")
        st.metric("Status", "OK")

# ==========================================
# TAB 3: LAYOUT
# ==========================================
with tab_layout:
    st.header("📐 Layout: Jak to poskládat")
    st.markdown("Aby aplikace nevypadala jako dlouhá nudle, musíme ji strukturovat.")

    # --- COLUMNS ---
    st.subheader("1. Sloupce (`st.columns`)")
    st.code("""
col1, col2 = st.columns(2)

with col1:
    st.write("Vlevo")

with col2:
    st.write("Vpravo")
    """, language="python")
    
    c1, c2 = st.columns(2)
    with c1:
        st.info("Vlevo")
    with c2:
        st.warning("Vpravo")

    st.divider()

    # --- TABS ---
    st.subheader("2. Záložky (`st.tabs`)")
    st.code("""
tab1, tab2 = st.tabs(["Grafy", "Data"])

with tab1:
    st.write("Tady bude graf")

with tab2:
    st.write("Tady bude tabulka")
    """, language="python")
    
    t1, t2 = st.tabs(["Grafy", "Data"])
    with t1:
        st.write("📈 Graf...")
    with t2:
        st.write("📋 Tabulka...")

    st.divider()

    # --- SIDEBAR ---
    st.subheader("3. Postranní panel (`st.sidebar`)")
    st.markdown("Ideální pro filtry a nastavení.")
    st.code("""
st.sidebar.header("Filtry")
st.sidebar.write("Tohle je vlevo.")
    """, language="python")
    st.info("Podívejte se doleva! (V této demo aplikaci už sidebar je).")

    st.divider()

    # --- EXPANDER ---
    st.subheader("4. Expander (Rozbalovátko)")
    st.code("""
with st.expander("Klikni pro více info"):
    st.write("Tady je schovaný text.")
    """, language="python")
    with st.expander("Klikni pro více info"):
        st.write("Tady je schovaný text.")

# ==========================================
# TAB 4: DATA A GRAFY
# ==========================================
with tab_data:
    st.header("📈 Zobrazení Dat")
    
    # Data pro ukázku
    df_demo = pd.DataFrame({
        'Palivo': ['Natural 95', 'Nafta', 'LPG'],
        'Cena': [38.5, 37.2, 17.5]
    })

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tabulky (`dataframe`)")
        st.markdown("Interaktivní tabulka. Můžeme skrýt index pro čistší vzhled.")
        st.code("""
# Zobrazení bez indexu (0, 1, 2...)
st.dataframe(df, hide_index=True)
        """, language="python")
        st.dataframe(df_demo, hide_index=True)
        
    with col2:
        st.subheader("Grafy (`altair_chart`)")
        st.markdown("Vložení Altair grafu.")
        st.code("""
chart = alt.Chart(df).mark_bar().encode(...)
st.altair_chart(chart, use_container_width=True)
        """, language="python")
        
        c = alt.Chart(df_demo).mark_bar().encode(x='Palivo', y='Cena')
        st.altair_chart(c, use_container_width=True)

# ==========================================
# TAB 5: STAVBA DASHBOARDU
# ==========================================
with tab_challenge:
    st.header("🚀 Kuchařka pro váš Dashboard")
    st.markdown("Otevřete si svůj soubor a skládejte si aplikaci z těchto bloků.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Stavební bloky")
        
        show_imports = st.checkbox("1. Importy", value=True, key="pd_imp_final")
        show_config = st.checkbox("2. Konfigurace stránky", value=True, key="pd_load_final")
        show_title = st.checkbox("3. Nadpis", value=True)
        show_data = st.checkbox("4. Načtení dat")
        show_kpi = st.checkbox("5. Klíčové ukazatele (Metriky)")
        show_layout = st.checkbox("6. Layout (Sloupce, Záložky)")
        show_chart = st.checkbox("7. Graf")
        show_table = st.checkbox("8. Tabulka")

    with col2:
        st.subheader("Výsledný kód")
        
        code_parts = []
        
        if show_imports:
            code_parts.append('''
# --- 1. IMPORTY ---
import streamlit as st
import pandas as pd
import altair as alt
''')
        if show_config:
            code_parts.append('''
# --- 2. KONFIGURACE STRÁNKY ---
st.set_page_config(layout="wide", page_title="Ceny PHM")
''')
        if show_title:
            code_parts.append('''
# --- 3. NADPIS ---
st.title("⛽ Vývoj cen pohonných hmot")
''')
        if show_data:
            code_parts.append('''
# --- 4. NAČTENÍ DAT ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/CENPHMT.csv")
    df.rename(columns={'Hodnota': 'Cena', 'CASTPHM': 'Tydentext', 'Druh PHM': 'Produkt'}, inplace=True)
    df['Datum'] = pd.to_datetime(df['Tydentext'] + '-1', format='%Y-W%W-%w')
    df = df[df['IndicatorType'] == '6621T']
    return df

df = load_data()
''')
        if show_kpi:
            code_parts.append('''
# --- 5. KLÍČOVÉ UKAZATELE (METRIKY) ---
latest_price = df.loc[df['Datum'].idxmax()]['Cena']
st.metric("Poslední cena", f"{latest_price:.2f} Kč")
''')
        if show_layout:
            code_parts.append('''
# --- 6. LAYOUT ---
# col1, col2 = st.columns(2)
# tab1, tab2 = st.tabs(["Grafy", "Data"])
''')
        if show_chart:
            code_parts.append('''
# --- 7. GRAF ---
chart = alt.Chart(df).mark_line().encode(x='Datum:T', y='Cena:Q', color='Produkt:N')
st.altair_chart(chart, use_container_width=True)
''')
        if show_table:
            code_parts.append('''
# --- 8. TABULKA ---
st.dataframe(df, hide_index=True)
''')

        st.code("".join(code_parts), language="python")
