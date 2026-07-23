def load_css():
    return """
<style>

/*=====================================================
  FINPULSE TERMINAL v2
  Theme Foundation
=====================================================*/

/*-----------------------------------------------------
  Hide Streamlit UI
-----------------------------------------------------*/

#MainMenu,
header,
footer{
    visibility:hidden;
}

.stDeployButton{
    display:none;
}

/*-----------------------------------------------------
  Root Variables
-----------------------------------------------------*/

:root{

    --bg:#0B0F19;
    --surface:#111827;
    --surface-2:#172033;

    --border:#1F2937;
    --border-light:#374151;

    --primary:#22C55E;
    --primary-soft:rgba(34,197,94,.12);

    --text:#F8FAFC;
    --muted:#94A3B8;
    --subtle:#6B7280;

    --radius:16px;

    --shadow-sm:
        0 6px 18px rgba(0,0,0,.18);

    --shadow:
        0 12px 30px rgba(0,0,0,.28);

    --shadow-green:
        0 12px 30px rgba(34,197,94,.14);

    --transition:.24s cubic-bezier(.4,0,.2,1);

}

/*-----------------------------------------------------
  Global
-----------------------------------------------------*/

html{

    scroll-behavior:smooth;

}

html,
body,
.stApp{

    background:var(--bg);

    color:var(--text);

    font-family:
        "Inter",
        "SF Pro Display",
        sans-serif;

    background-image:

        linear-gradient(
            rgba(255,255,255,.022) 1px,
            transparent 1px
        ),

        linear-gradient(
            90deg,
            rgba(255,255,255,.022) 1px,
            transparent 1px
        );

    background-size:36px 36px;

    animation:pageFade .45s ease;

}

/*-----------------------------------------------------
  Layout
-----------------------------------------------------*/

.block-container{

    max-width:97%;

    padding-top:.9rem;

    padding-bottom:2.2rem;

}

section.main{

    animation:fadeUp .45s ease;

}

/*-----------------------------------------------------
  Universal Transitions
-----------------------------------------------------*/

*{

    transition:

        background-color var(--transition),

        border-color var(--transition),

        color var(--transition),

        box-shadow var(--transition),

        transform var(--transition);

}

/*=====================================================
  Scrollbar
=====================================================*/

::-webkit-scrollbar{

    width:10px;

}

::-webkit-scrollbar-track{

    background:#0E1523;

}

::-webkit-scrollbar-thumb{

    background:#344155;

    border-radius:999px;

}

::-webkit-scrollbar-thumb:hover{

    background:var(--primary);

}

/*=====================================================
  Animations
=====================================================*/

@keyframes pageFade{

    from{

        opacity:0;

    }

    to{

        opacity:1;

    }

}

@keyframes fadeUp{

    from{

        opacity:0;

        transform:

            translateY(14px);

    }

    to{

        opacity:1;

        transform:

            translateY(0);

    }

}

@keyframes blink{

    50%{

        opacity:0;

    }

}

@keyframes glow{

    0%{

        box-shadow:0 0 0 rgba(34,197,94,0);

    }

    50%{

        box-shadow:

            0 0 18px rgba(34,197,94,.12);

    }

    100%{

        box-shadow:0 0 0 rgba(34,197,94,0);

    }

}

@keyframes floatUp{

    0%{

        transform:

            translateY(2px);

    }

    100%{

        transform:

            translateY(-2px);

    }

}

/*=====================================================
  Header
=====================================================*/

.terminal-title{

    color:var(--text);

    font-size:40px;

    font-weight:900;

    letter-spacing:4px;

    line-height:1.1;

    margin-bottom:2px;

    text-shadow:

        0 0 12px rgba(34,197,94,.10);

}

.terminal-subtitle{

    color:var(--muted);

    font-size:15px;

    line-height:1.7;

    margin-top:8px;

    margin-bottom:28px;

}

.cursor{

    color:var(--primary);

    animation:

        blink 1s infinite;

}

/*=====================================================
  Generic Containers
=====================================================*/

[data-testid="stVerticalBlockBorderWrapper"]{

    border-radius:var(--radius);

    border:1px solid transparent;

    overflow:hidden;

}

[data-testid="stVerticalBlockBorderWrapper"]:hover{

    border-color:rgba(34,197,94,.25);

    box-shadow:

        var(--shadow-green);

    transform:

        translateY(-2px);

}

/*=====================================================
  Section Titles
=====================================================*/

.panel-title{

    position:relative;

    color:var(--text);

    font-size:22px;

    font-weight:800;

    padding-left:16px;

    margin-top:24px;

    margin-bottom:22px;

    border-left:

        5px solid var(--primary);

}

.panel-title::after{

    content:"";

    position:absolute;

    left:16px;

    bottom:-8px;

    width:82px;

    height:2px;

    background:var(--primary);

    border-radius:999px;

}

.small-title{

    color:var(--muted);

    font-size:12px;

    font-weight:700;

    letter-spacing:.18em;

    text-transform:uppercase;

}

/*=====================================================
  Metric Cards
=====================================================*/

[data-testid="stMetric"]{

    background:rgba(17,24,39,.82);

    backdrop-filter:blur(18px);

    border:1px solid rgba(255,255,255,.05);

    border-radius:var(--radius);

    padding:18px;

    margin-bottom:14px;

    animation:fadeUp .45s ease;

    box-shadow:var(--shadow-sm);

}

[data-testid="stMetric"]:hover{

    transform:
        translateY(-4px)
        scale(1.01);

    border-color:var(--primary);

    box-shadow:
        var(--shadow-green);

}

[data-testid="stMetricLabel"]{

    color:var(--muted);

    font-weight:600;

    letter-spacing:.05em;

}

[data-testid="stMetricValue"]{

    color:var(--text);

    font-size:32px;

    font-weight:800;

    line-height:1.15;

}

[data-testid="stMetricDelta"]{

    font-weight:700;

}

/*=====================================================
  Buttons
=====================================================*/

.stButton>button{

    width:100%;

    height:46px;

    border-radius:14px;

    background:var(--surface);

    border:1px solid var(--border-light);

    color:var(--text);

    font-weight:700;

    cursor:pointer;

    box-shadow:var(--shadow-sm);

}

.stButton>button:hover{

    background:var(--surface-2);

    border-color:var(--primary);

    transform:translateY(-2px);

    box-shadow:var(--shadow-green);

}

.stButton>button:active{

    transform:scale(.98);

}

/*=====================================================
  Inputs
=====================================================*/

.stTextInput input,
.stNumberInput input{

    background:var(--surface) !important;

    color:var(--text) !important;

    border:1px solid var(--border-light) !important;

    border-radius:14px !important;

    padding:.55rem .9rem !important;

}

.stTextInput input:focus,
.stNumberInput input:focus{

    border-color:var(--primary) !important;

    box-shadow:
        0 0 0 3px rgba(34,197,94,.12);

}

/*=====================================================
  Selectbox
=====================================================*/

.stSelectbox div[data-baseweb="select"]{

    border-radius:14px;

}

.stSelectbox div[data-baseweb="select"]:hover{

    border-color:var(--primary);

}

.stSelectbox *{

    color:var(--text);

}

/*=====================================================
  Multiselect
=====================================================*/

.stMultiSelect div[data-baseweb="select"]{

    border-radius:14px;

}

.stMultiSelect div[data-baseweb="select"]:hover{

    border-color:var(--primary);

}

/*=====================================================
  Slider
=====================================================*/

.stSlider{

    padding-top:.4rem;

}

.stSlider [role="slider"]{

    background:var(--primary);

    border:none;

}

.stSlider [data-baseweb="slider"]>div:nth-child(2){

    background:var(--primary);

}

/*=====================================================
  Tabs
=====================================================*/

.stTabs{

    margin-top:.4rem;

}

.stTabs [data-baseweb="tab-list"]{

    gap:.45rem;

    border-bottom:none;

}

.stTabs [data-baseweb="tab"]{

    background:transparent;

    color:var(--muted);

    padding:.6rem 1rem;

    border-radius:12px;

    font-weight:600;

}

.stTabs [data-baseweb="tab"]:hover{

    color:var(--text);

    background:rgba(255,255,255,.03);

}

.stTabs [aria-selected="true"]{

    background:rgba(34,197,94,.12);

    color:var(--primary);

    border:1px solid rgba(34,197,94,.25);

    transform:translateY(-2px);

}

/*=====================================================
  Dataframes
=====================================================*/

[data-testid="stDataFrame"]{

    border-radius:18px;

    overflow:hidden;

    border:1px solid var(--border);

    background:var(--surface);

    animation:fadeUp .45s ease;

    box-shadow:var(--shadow-sm);

}

[data-testid="stDataFrame"]:hover{

    box-shadow:var(--shadow-green);

}

[data-testid="stDataFrame"] table{

    border-collapse:collapse;

}

[data-testid="stDataFrame"] tbody tr{

    transition:background .18s ease;

}

[data-testid="stDataFrame"] tbody tr:hover{

    background:rgba(34,197,94,.05);

}

/*=====================================================
  Plotly Charts
=====================================================*/

.js-plotly-plot{

    border-radius:18px;

    overflow:hidden;

}

.js-plotly-plot:hover{

    transform:translateY(-2px);

}

/*=====================================================
  Alerts
=====================================================*/

[data-testid="stAlert"]{

    border-radius:16px;

    border:none;

    overflow:hidden;

    animation:fadeUp .35s ease;

    box-shadow:var(--shadow-sm);

}

/*=====================================================
  Expanders
=====================================================*/

details{

    border-radius:16px;

    overflow:hidden;

}

summary{

    font-weight:600;

}

/*=====================================================
  Divider
=====================================================*/

hr{

    border:none;

    border-top:1px solid var(--border);

    margin:2rem 0;

    opacity:.75;

}

/*=====================================================
  Live Market Ticker
=====================================================*/

.fp-ticker{

    width:100%;

    overflow:hidden;

    white-space:nowrap;

    border:1px solid var(--border);

    border-radius:16px;

    background:linear-gradient(
        90deg,
        rgba(17,24,39,.96),
        rgba(13,19,32,.96)
    );

    padding:12px 0;

    margin-bottom:22px;

    box-shadow:var(--shadow-sm);

}

.fp-ticker-track{

    display:inline-flex;

    align-items:center;

    gap:48px;

    animation:tickerScroll 45s linear infinite;

}

.fp-ticker:hover .fp-ticker-track{

    animation-play-state:paused;

}

.fp-ticker-item{

    display:flex;

    align-items:center;

    gap:10px;

    color:var(--text);

    font-size:14px;

    font-weight:600;

}

.fp-ticker-item:hover{

    color:white;

}

.fp-dot{

    width:8px;

    height:8px;

    border-radius:999px;

    background:var(--primary);

    box-shadow:0 0 10px rgba(34,197,94,.5);

}

@keyframes tickerScroll{

    from{

        transform:translateX(0);

    }

    to{

        transform:translateX(-50%);

    }

}

/*=====================================================
  News Cards
=====================================================*/

.fp-news-card{

    background:rgba(17,24,39,.82);

    border:1px solid rgba(255,255,255,.05);

    border-radius:16px;

    padding:18px;

    margin-bottom:16px;

    box-shadow:var(--shadow-sm);

    animation:fadeUp .45s ease;

}

.fp-news-card:hover{

    transform:translateY(-3px);

    border-color:rgba(34,197,94,.3);

    box-shadow:var(--shadow-green);

}

.fp-news-title{

    font-size:17px;

    font-weight:700;

    color:var(--text);

    margin-bottom:8px;

}

.fp-news-meta{

    color:var(--muted);

    font-size:13px;

    margin-bottom:12px;

}

.fp-news-summary{

    color:#CBD5E1;

    line-height:1.7;

    font-size:14px;

}

/*=====================================================
  Links
=====================================================*/

a{

    color:var(--primary);

    text-decoration:none;

}

a:hover{

    text-decoration:underline;

}

/*=====================================================
  Images
=====================================================*/

img{

    border-radius:14px;

}

/*=====================================================
  Sidebar (Future Ready)
=====================================================*/

section[data-testid="stSidebar"]{

    background:#0D1422;

    border-right:1px solid var(--border);

}

/*=====================================================
  Loading Spinner
=====================================================*/

.stSpinner{

    color:var(--primary);

}

/*=====================================================
  Footer
=====================================================*/

.footer{

    margin-top:40px;

    padding:26px;

    text-align:center;

    color:var(--subtle);

    font-size:13px;

    border-top:1px solid var(--border);

    opacity:.85;

}

.footer strong{

    color:var(--text);

}

.footer:hover{

    opacity:1;

}

/*=====================================================
  Utility Classes
=====================================================*/

.fp-card{

    background:rgba(17,24,39,.82);

    border:1px solid rgba(255,255,255,.05);

    border-radius:16px;

    padding:18px;

    box-shadow:var(--shadow-sm);

}

.fp-card:hover{

    border-color:rgba(34,197,94,.28);

    box-shadow:var(--shadow-green);

}

.fp-center{

    display:flex;

    justify-content:center;

    align-items:center;

}

.fp-gap{

    height:18px;

}

.fp-muted{

    color:var(--muted);

}

.fp-success{

    color:#22C55E;

}

.fp-danger{

    color:#EF4444;

}

.fp-warning{

    color:#F59E0B;

}

/*=====================================================
  Selection
=====================================================*/

::selection{

    background:rgba(34,197,94,.25);

    color:white;

}

/*=====================================================
  Responsive
=====================================================*/

@media (max-width:900px){

    .terminal-title{

        font-size:30px;

        letter-spacing:2px;

    }

    .panel-title{

        font-size:19px;

    }

    [data-testid="stMetricValue"]{

        font-size:26px;

    }

    .block-container{

        max-width:100%;

        padding-left:1rem;

        padding-right:1rem;

    }

}

/*-----------------------------------------------------
  Live Ticker
-----------------------------------------------------*/

.fp-ticker-rule{
    border:none;
    border-top:2px solid #22C55E;
    opacity:.55;
    margin:0;
}

.fp-ticker-wrap{
    width:100%;
    overflow:hidden;
    background:#0B1420;
    padding:10px 0;
    white-space:nowrap;
}

.fp-ticker-track{
    display:inline-block;
    white-space:nowrap;
    animation:fp-scroll 45s linear infinite;
}

.fp-ticker-wrap:hover .fp-ticker-track{
    animation-play-state:paused;
}

@keyframes fp-scroll{
    from{transform:translateX(0);}
    to{transform:translateX(-50%);}
}

.fp-ticker-item{
    display:inline-block;
    padding:0 28px;
    font-family:monospace;
    font-size:.94rem;
    font-weight:600;
    color:#E5E7EB;
}

.fp-ticker-up{
    color:#22C55E;
}

.fp-ticker-down{
    color:#EF4444;
}

/*-----------------------------------------------------
  Section Titles & Dividers
-----------------------------------------------------*/

.panel-title{
    font-size:1.35rem;
    font-weight:800;
    letter-spacing:.05em;
    text-transform:uppercase;
    margin-bottom:18px;
    color:#F9FAFB;
}

.fp-section-gap{
    border:none;
    border-top:1px solid #1F2937;
    width:100%;
    margin:60px 0;
    opacity:.65;
}

/*-----------------------------------------------------
  Market Summary
-----------------------------------------------------*/

.fp-overview-box{
    background:#111827;
    border:1px solid #1F2937;
    border-left:4px solid #22C55E;
    border-radius:12px;
    padding:26px;
    margin-bottom:8px;
}

.fp-overview-box [data-testid="stMetricValue"]{
    font-size:2rem;
}

/*-----------------------------------------------------
  Equity Workspace
-----------------------------------------------------*/

.fp-workspace-box{
    background:#0F172A;
    border:1px solid rgba(34,197,94,.20);
    border-left:4px solid #22C55E;
    border-radius:16px;
    padding:30px;
    margin-bottom:12px;
    box-shadow:0 6px 18px rgba(0,0,0,.18);
}

.fp-workspace-title{
    font-size:1.35rem;
    font-weight:800;
    letter-spacing:.05em;
    text-transform:uppercase;
    color:#F9FAFB;
}

.fp-workspace-sub{
    color:#6B7280;
    font-size:.88rem;
    margin-top:4px;
    margin-bottom:18px;
}

.fp-watchlist-chip{
    background:#111827;
    border:1px solid #1F2937;
    border-radius:10px;
    padding:10px 14px;
    margin-top:10px;
    color:#D1D5DB;
    font-size:.9rem;
}

/*-----------------------------------------------------
  Tabs
-----------------------------------------------------*/

.stTabs [data-baseweb="tab-list"]{
    gap:8px;
    background:#0B1420;
    border:1px solid #1F2937;
    border-radius:12px;
    padding:8px;
    margin-bottom:20px;
}

.stTabs [data-baseweb="tab"]{
    height:50px;
    padding:0 24px;
    border-radius:8px;
    font-size:.9rem;
    font-weight:700;
    color:#9CA3AF;
    background:transparent;
    border:1px solid transparent;
    text-transform:uppercase;
}

.stTabs [data-baseweb="tab"]:hover{
    background:#111827;
    color:#F3F4F6;
}

.stTabs [aria-selected="true"]{
    background:#163A24 !important;
    border:1px solid #22C55E !important;
    color:#22C55E !important;
}

.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"]{
    display:none;
}

/*-----------------------------------------------------
  News
-----------------------------------------------------*/

.fp-news-card{
    background:#111827;
    border:1px solid #1F2937;
    border-left:3px solid #22C55E;
    border-radius:8px;
    padding:12px 15px;
    margin-bottom:10px;
}

.fp-news-headline{
    color:#F3F4F6;
    font-size:.9rem;
    font-weight:700;
    line-height:1.35;
    margin-bottom:8px;
}

.fp-news-meta{
    display:flex;
    justify-content:space-between;
    color:#6B7280;
    font-size:.78rem;
}

/*=====================================================
  End
=====================================================*/

</style>
"""