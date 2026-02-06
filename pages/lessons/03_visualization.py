import streamlit as st
import pandas as pd
import altair as alt
import streamlit.components.v1 as components

# --- Konfigurace a Data ---
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
st.title("📊 Altair Masterclass: Ceny pohonných hmot")
st.caption("Vizualizujeme reálná data o cenách paliv z ČSÚ.")

# --- Navigace ---
tab_intro, tab_theory, tab_basic, tab_adv, tab_agg, tab_challenge = st.tabs([
    "🎬 PREZENTACE",
    "1. Teorie (Gramatika)", 
    "2. Základní grafy", 
    "3. Vylepšování", 
    "4. Agregace v grafu", 
    "🚀 KUCHAŘKA GRAFŮ"
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
    <title>Altair Visuals Demo</title>
    
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
                        <div class="inline-block px-3 py-1 bg-orange-500/20 text-orange-300 rounded-full text-sm font-mono mb-6 border border-orange-500/30">
                            import altair as alt
                        </div>
                        <h1>Altair 📊<br><span class="text-orange-400">Gramatika Grafiky</span></h1>
                        <p class="mt-6 text-xl">
                            Zapomeňte na kreslení čar a bodů. S Altairem <strong>popisujete</strong>, co chcete vidět. Je to deklarativní knihovna, která mluví jazykem dat.
                        </p>
                        <ul class="mt-8 space-y-4 text-slate-300">
                            <li class="flex items-center gap-3">
                                <i class="fas fa-cubes text-yellow-400"></i> Skládání grafů jako Lego
                            </li>
                            <li class="flex items-center gap-3">
                                <i class="fas fa-mouse-pointer text-blue-400"></i> Interaktivita na jeden řádek
                            </li>
                            <li class="flex items-center gap-3">
                                <i class="fas fa-globe text-green-400"></i> Web-ready (JSON formát)
                            </li>
                        </ul>
                    </div>
                    <div class="flex items-center justify-center">
                        <i class="fas fa-chart-area text-[15rem] text-orange-500/20 animate-pulse"></i>
                    </div>
                </div>
                <div class="card-footer p-6 border-t border-slate-700 bg-slate-800/50 flex justify-between text-slate-500 font-mono text-sm">
                    <span>vega-lite wrapper</span>
                    <span>Použij šipky ➝</span>
                </div>
            </div>
        </div>

        <!-- SLIDE 1: FILOSOFIE -->
        <div class="slide next" id="slide-1">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-slate-200 font-bold">1. Filosofie (Grammar of Graphics)</h3>
                    <i class="fas fa-brain text-orange-400"></i>
                </div>
                <div class="card-body">
                    <div>
                        <div class="feature-icon bg-orange-500/20 text-orange-400"><i class="fas fa-project-diagram"></i></div>
                        <h2>Mapování, ne kreslení</h2>
                        <p>V Excelu vyberete buňky a kliknete na "Graf". V Altairu definujete vztahy.</p>
                        <p>Každý graf se skládá ze tří částí:</p>
                        <ul class="space-y-2 text-slate-300 ml-4">
                            <li><strong>1. Data:</strong> Tabulka (DataFrame)</li>
                            <li><strong>2. Mark:</strong> Geometrický tvar (sloupec, bod, čára)</li>
                            <li><strong>3. Encoding:</strong> Propojení sloupců dat s vizuálními vlastnostmi (osa X, osa Y, barva, velikost).</li>
                        </ul>
                    </div>
                    <div class="flex items-center justify-center">
                        <div class="grid grid-cols-1 gap-4 w-full max-w-md">
                            <div class="p-4 bg-slate-800 border border-slate-600 rounded-lg text-center">DATA</div>
                            <div class="flex justify-center"><i class="fas fa-arrow-down text-slate-500"></i></div>
                            <div class="p-4 bg-slate-800 border border-slate-600 rounded-lg text-center">ENCODING (X, Y, Color)</div>
                            <div class="flex justify-center"><i class="fas fa-arrow-down text-slate-500"></i></div>
                            <div class="p-4 bg-orange-600/20 border border-orange-500 text-orange-300 rounded-lg text-center font-bold">VIZUALIZACE</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 2: SYNTAXE -->
        <div class="slide next" id="slide-2">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-slate-200 font-bold">2. Deklarativní Syntaxe</h3>
                    <i class="fas fa-code text-orange-400"></i>
                </div>
                <div class="card-body">
                    <div>
                        <div class="feature-icon bg-blue-500/20 text-blue-400"><i class="fas fa-laptop-code"></i></div>
                        <h2>Čitelný kód</h2>
                        <p>Kód Altairu se čte jako věta. <em>"Vezmi graf, použij data, udělej body a namapuj osu X na 'Cena' a osu Y na 'Množství'."</em></p>
                        <p>Díky tomu se snadno učí a ještě snáze upravuje.</p>
                    </div>
                    <div class="code-window">
                        <div class="code-header">
                            <div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div>
                        </div>
                        <div class="code-content">
                            <span class="kwd">import</span> altair <span class="kwd">as</span> alt<br><br>
                            chart = alt.<span class="func">Chart</span>(data).<span class="func">mark_circle</span>().<span class="func">encode</span>(<br>
                            &nbsp;&nbsp;x=<span class="str">'Cena'</span>,<br>
                            &nbsp;&nbsp;y=<span class="str">'Mnozstvi'</span>,<br>
                            &nbsp;&nbsp;color=<span class="str">'Kategorie'</span>,<br>
                            &nbsp;&nbsp;size=<span class="str">'Zisk'</span>,<br>
                            &nbsp;&nbsp;tooltip=[<span class="str">'Produkt'</span>, <span class="str">'Cena'</span>]<br>
                            )
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 3: INTERAKTIVITA -->
        <div class="slide next" id="slide-3">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-slate-200 font-bold">3. Interaktivita</h3>
                    <i class="fas fa-hand-pointer text-orange-400"></i>
                </div>
                <div class="card-body">
                    <div>
                        <div class="feature-icon bg-purple-500/20 text-purple-400"><i class="fas fa-magic"></i></div>
                        <h2>Živé grafy</h2>
                        <p>Statické obrázky jsou nuda. Uživatelé chtějí data prozkoumat. Zoomovat, posouvat, filtrovat.</p>
                        <p>V Altairu stačí přidat jedinou metodu <code>.interactive()</code> a graf ožije. Žádný JavaScript, žádné složité callbacky.</p>
                    </div>
                    <div class="code-window">
                        <div class="code-header">
                            <div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div>
                        </div>
                        <div class="code-content">
                            <span class="comment"># Statický graf</span><br>
                            graf = alt.Chart(df).mark_line().encode(...)<br><br>
                            <span class="comment"># INTERAKTIVNÍ GRAF (Zoom & Pan)</span><br>
                            zivy_graf = graf.<span class="func">interactive</span>()<br><br>
                            <span class="comment"># Tooltipy (Bubliny po najetí myší)</span><br>
                            <span class="comment"># Stačí přidat parametr tooltip=['sloupec']</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SLIDE 4: TYPY GRAFŮ -->
        <div class="slide next" id="slide-4">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-slate-200 font-bold">4. Stavebnice</h3>
                    <i class="fas fa-shapes text-orange-400"></i>
                </div>
                <div class="card-body">
                    <div>
                        <div class="feature-icon bg-green-500/20 text-green-400"><i class="fas fa-layer-group"></i></div>
                        <h2>Jeden princip, všechna data</h2>
                        <p>Nemusíte se učit 50 různých funkcí pro 50 typů grafů. Stačí změnit <code>mark</code> a <code>encoding</code>.</p>
                        <p>Chcete sloupcový graf místo čárového? Změňte <code>mark_line()</code> na <code>mark_bar()</code>. Hotovo.</p>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div class="p-4 bg-slate-800 rounded border border-slate-700 flex items-center gap-3">
                            <i class="fas fa-chart-bar text-orange-400"></i> <span>mark_bar()</span>
                        </div>
                        <div class="p-4 bg-slate-800 rounded border border-slate-700 flex items-center gap-3">
                            <i class="fas fa-chart-line text-blue-400"></i> <span>mark_line()</span>
                        </div>
                        <div class="p-4 bg-slate-800 rounded border border-slate-700 flex items-center gap-3">
                            <i class="fas fa-dot-circle text-purple-400"></i> <span>mark_circle()</span>
                        </div>
                        <div class="p-4 bg-slate-800 rounded border border-slate-700 flex items-center gap-3">
                            <i class="fas fa-map-marker-alt text-red-400"></i> <span>mark_geoshape()</span>
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
            <button onclick="toggleFullscreen()" class="w-12 h-12 rounded-full bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center transition border border-slate-600 focus:outline-none focus:ring-2 focus:ring-orange-500 cursor-pointer" title="Fullscreen">
                <i class="fas fa-expand"></i>
            </button>
            <button onclick="prevSlide()" class="w-12 h-12 rounded-full bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center transition border border-slate-600 focus:outline-none cursor-pointer">
                <i class="fas fa-arrow-left"></i>
            </button>
            <button onclick="nextSlide()" class="w-12 h-12 rounded-full bg-orange-600 hover:bg-orange-500 text-white flex items-center justify-center transition shadow-lg shadow-orange-900/50 focus:outline-none cursor-pointer">
                <i class="fas fa-arrow-right"></i>
            </button>
        </div>
    </div>

    <!-- Progress Bar -->
    <div class="fixed top-0 left-0 h-1 bg-slate-800 w-full z-50">
        <div id="progress-bar" class="h-full bg-orange-500 transition-all duration-300" style="width: 20%"></div>
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
# TAB 1: TEORIE
# ==========================================
with tab_theory:
    st.header("🧠 Grammar of Graphics")
    st.markdown("""
    Altair není o tom, že si pamatujete názvy funkcí. Je o tom, že graf **popíšete**.
    Každý graf se skládá ze 3 hlavních částí:
    """)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("**1. DATA**")
        st.write("Tabulka (DataFrame), kterou chceme vizualizovat.")
    with c2:
        st.info("**2. MARK (Značka)**")
        st.write("Jak data zobrazíme? (Tečka, Čára, Sloupec...)")
    with c3:
        st.info("**3. ENCODING (Mapování)**")
        st.write("Který sloupec patří na osu X? Který na Y? Který určuje barvu?")

    st.divider()
    
    st.subheader("Syntaxe v Pythonu")
    st.code("""
alt.Chart(DATA).mark_TYP_GRAFU().encode(
    x='SLOUPEC_PRO_OSU_X',
    y='SLOUPEC_PRO_OSU_Y',
    color='SLOUPEC_PRO_BARVU'
)
    """, language="python")
    
    st.caption("Příklad: `alt.Chart(df).mark_bar().encode(x='Produkt', y='Cena')`")

# ==========================================
# TAB 2: ZÁKLADNÍ GRAFY
# ==========================================
with tab_basic:
    st.header("📈 Základní typy grafů")
    
    # --- BAR CHART ---
    st.subheader("A) Bar Chart (Sloupcový)")
    st.markdown("Ideální pro porovnání kategorií.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.code("""
alt.Chart(df).mark_bar().encode(
    x='Produkt',
    y='Cena'
)
        """, language="python")
    with col2:
        c = alt.Chart(df).mark_bar().encode(x='Produkt', y='Cena')
        st.altair_chart(c, use_container_width=True)

    st.divider()

    # --- LINE CHART ---
    st.subheader("B) Line Chart (Čárový)")
    st.markdown("Ideální pro vývoj v čase.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.code("""
alt.Chart(df).mark_line().encode(
    x='Datum',
    y='Cena'
)
        """, language="python")
    with col2:
        c = alt.Chart(df).mark_line().encode(x='Datum', y='Cena')
        st.altair_chart(c, use_container_width=True)

# ==========================================
# TAB 3: VYLEPŠOVÁNÍ
# ==========================================
with tab_adv:
    st.header("🎨 Vylepšování grafů")
    st.markdown("Grafy musí být nejen správné, ale i hezké a čitelné.")

    # --- BARVY ---
    st.subheader("1. Barvy a Legenda")
    st.markdown("Přidáme `color`, aby se data rozlišila.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.code("""
alt.Chart(df).mark_line().encode(
    x='Datum',
    y='Cena',
    color='Produkt' # Automaticky vytvoří legendu
)
        """, language="python")
    with col2:
        c = alt.Chart(df).mark_line().encode(
            x='Datum', y='Cena', color='Produkt'
        )
        st.altair_chart(c, use_container_width=True)

# ==========================================
# TAB 4: AGREGACE V GRAFU
# ==========================================
with tab_agg:
    st.header("∑ Agregace přímo v grafu")
    st.markdown("""
    Altair je chytrý. Nemusíte data seskupovat v Pandas (groupby), můžete to říct přímo grafu!
    Používá se syntaxe: `'funkce(sloupec)'`.
    """)

    # --- SUMA ---
    st.subheader("Průměr (mean)")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.code("""
alt.Chart(df).mark_bar().encode(
    x='Produkt',
    y='mean(Cena)' # Průměrná cena
)
        """, language="python")
    with col2:
        c = alt.Chart(df).mark_bar().encode(x='Produkt', y='mean(Cena)')
        st.altair_chart(c, use_container_width=True)

# ==========================================
# TAB 5: KUCHAŘKA GRAFŮ
# ==========================================
with tab_challenge:
    st.header("🚀 Kuchařka grafů pro Dashboard")

    chart_type = st.radio(
        "Vyberte typ grafu:",
        ["Vývoj ceny v čase", "Srovnání paliv"]
    )
    
    if "Vývoj ceny" in chart_type:
        st.info("Ukazuje vývoj ceny vybraného druhu paliva v čase.")
        produkt = st.selectbox("Vyberte druh paliva:", df['Produkt'].unique())
        
        code = f"""
chart = alt.Chart(df[df['Produkt'] == '{produkt}']).mark_line(point=True).encode(
    x='Datum:T',
    y='Cena:Q',
    tooltip=['Datum', 'Cena']
).interactive()
"""
        st.code(code, language="python")
        chart = alt.Chart(df[df['Produkt'] == produkt]).mark_line(point=True).encode(
            x='Datum:T', y='Cena:Q', tooltip=['Datum', 'Cena']
        ).interactive()
        st.altair_chart(chart, use_container_width=True)

    elif "Srovnání paliv" in chart_type:
        st.info("Porovnává průměrnou cenu různých druhů paliv za celé období.")
        
        code = """
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('Produkt', sort='-y'),
    y='mean(Cena)',
    color='Produkt'
).interactive()
"""
        st.code(code, language="python")
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Produkt', sort='-y'), y='mean(Cena)', color='Produkt'
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
