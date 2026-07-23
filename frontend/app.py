import os
import streamlit as st
import pandas as pd
import requests

from news import display_market_news
from radar import create_dna_radar
from financials import display_key_financials
from styles import load_css
from components import header, spotlight_card, footer

from charts import (
    create_price_chart,
    create_market_cap_chart,
    create_pe_chart,
    create_sector_chart,
    calculate_portfolio,
    calculate_dna,
)

# =====================================================
# PAGE CONFIG
# =====================================================

try:
    API_URL = st.secrets.get("API_URL", os.environ.get("API_URL", "http://127.0.0.1:8000"))
except Exception:
    API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="FinPulse Terminal",
    page_icon="📈",
    layout="wide",
)

st.markdown(load_css(), unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

header()

# =====================================================
# SESSION STATE
# =====================================================

if "watchlist" not in st.session_state:
    try:
        response = requests.get(f"{API_URL}/watchlist")
        response.raise_for_status()
        st.session_state.watchlist = response.json()
    except Exception:
        st.session_state.watchlist = []

# =====================================================
# FETCH MARKET DATA
# =====================================================

try:

    response = requests.get(f"{API_URL}/stocks")

    response.raise_for_status()

    df = pd.DataFrame(response.json())

except Exception as e:

    st.error("Unable to connect to the FinPulse backend.")

    st.exception(e)

    st.stop()

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def format_market_cap(value):

    if pd.isna(value):
        return "-"

    thresholds = [
        (1e12, "T"),
        (1e9, "B"),
        (1e6, "M"),
    ]

    for limit, suffix in thresholds:

        if value >= limit:
            return f"₹{value/limit:.2f}{suffix}"

    return f"₹{value:,.0f}"


def calculate_change(row):

    previous = row.get("prev_close", row["price"])

    if previous in [0, None]:
        return 0

    return ((row["price"] - previous) / previous) * 100


df["Change"] = df.apply(
    calculate_change,
    axis=1,
)

# =====================================================
# MARKET STATISTICS
# =====================================================

avg_pe = df["pe_ratio"].mean()

largest_company = df.loc[
    df["market_cap"].idxmax()
]

total_market_cap = df["market_cap"].sum()

gainers = (df["Change"] > 0).sum()

losers = (df["Change"] < 0).sum()

avg_change = df["Change"].mean()

top_gainer = df.loc[
    df["Change"].idxmax()
]

top_loser = df.loc[
    df["Change"].idxmin()
]

bullish_percent = (
    gainers / len(df)
) * 100

if bullish_percent >= 75:

    mood = "🚀 Very Bullish"

elif bullish_percent >= 55:

    mood = "📈 Bullish"

elif bullish_percent >= 45:

    mood = "⚖ Neutral"

elif bullish_percent >= 25:

    mood = "📉 Bearish"

else:

    mood = "💥 Very Bearish"

# =====================================================
# LIVE MARKET TICKER
# =====================================================

st.markdown(
    '<hr class="fp-ticker-rule">',
    unsafe_allow_html=True,
)

ticker_items = []

market_arrow = "▲" if avg_change >= 0 else "▼"
market_class = "fp-ticker-up" if avg_change >= 0 else "fp-ticker-down"

ticker_items.append(
    f'<span class="fp-ticker-item {market_class}">FINPULSE 20 {market_arrow}{avg_change:+.2f}%</span>'
)

market_df = df.sort_values("market_cap", ascending=False)

for _, row in market_df.iterrows():
    change = row["Change"]
    css_class = "fp-ticker-up" if change >= 0 else "fp-ticker-down"
    arrow = "▲" if change >= 0 else "▼"
    symbol = row["symbol"].replace(".NS", "")
    ticker_items.append(
        f'<span class="fp-ticker-item {css_class}">{symbol} {arrow} {change:+.2f}%</span>'
    )

ticker_html = "".join(ticker_items)

st.markdown(
    f"""
<div class="fp-ticker-wrap">
<div class="fp-ticker-track">

{ticker_html}

</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<hr class="fp-ticker-rule">',
    unsafe_allow_html=True,
)

# =====================================================
# MARKET SUMMARY
# =====================================================

st.markdown(
    '<div class="panel-title">📊 MARKET SUMMARY</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):

    # -------------------------------------------------
    # OVERVIEW
    # -------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "📈 Tracked Stocks",
            len(df),
        )

    with c2:
        st.metric(
            "📊 Average P/E",
            f"{avg_pe:.2f}",
        )

    with c3:
        st.metric(
            "👑 Market Leader",
            largest_company["symbol"].replace(".NS", ""),
        )

    with c4:
        st.metric(
            "💰 Market Cap",
            format_market_cap(total_market_cap),
        )

    st.divider()

    # -------------------------------------------------
    # TODAY'S PULSE
    # -------------------------------------------------

    p1, p2, p3, p4, p5 = st.columns(5)

    with p1:

        st.metric(
            "Market Mood",
            mood,
        )

    with p2:

        st.metric(
            "Top Gainer",
            top_gainer["symbol"].replace(".NS", ""),
            f"{top_gainer['Change']:+.2f}%"
        )

    with p3:

        st.metric(
            "Top Loser",
            top_loser["symbol"].replace(".NS", ""),
            f"{top_loser['Change']:+.2f}%"
        )

    with p4:

        st.metric(
            "Breadth",
            f"{gainers} ↑  {losers} ↓"
        )

    with p5:

        st.metric(
            "Average Move",
            f"{avg_change:+.2f}%"
        )

    st.divider()

    # -------------------------------------------------
    # MARKET INSIGHT
    # -------------------------------------------------

    if bullish_percent >= 70:

        insight = (
            "The market is showing broad bullish participation, with most tracked companies closing in positive territory. Momentum currently favors buyers."
        )

    elif bullish_percent <= 30:

        insight = (
            "Selling pressure dominates today's session. A majority of tracked companies are trading lower, indicating weak overall market sentiment."
        )

    else:

        insight = (
            "Market participation is balanced today, with neither buyers nor sellers establishing a decisive advantage."
        )

    st.info(
        f"💡 **Pulse Insight:** {insight}"
    )
# =====================================================
# MARKET TERMINAL
# =====================================================

st.markdown(
    '<div class="panel-title">📈 MARKET TERMINAL</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):

    st.caption(
        "Browse, search and compare every tracked company in real time."
    )

    search_col, sort_col = st.columns([5, 1.3])

    with search_col:

        search = st.text_input(
            "",
            placeholder="🔍 Search company, ticker or sector...",
            key="terminal_search",
            label_visibility="collapsed",
        )

    with sort_col:

        sort = st.selectbox(
            "",
            [
                "Market Cap",
                "Price",
                "P/E",
                "EPS",
            ],
            key="terminal_sort",
            label_visibility="collapsed",
        )

    terminal_df = df.copy()

    if search:

        query = search.lower()

        terminal_df = terminal_df[
            terminal_df["company"].str.lower().str.contains(query)
            |
            terminal_df["symbol"].str.lower().str.contains(query)
            |
            terminal_df["sector"].fillna("").str.lower().str.contains(query)
        ]

    sort_map = {
        "Market Cap": "market_cap",
        "Price": "price",
        "P/E": "pe_ratio",
        "EPS": "eps",
    }

    terminal_df = terminal_df.sort_values(
        sort_map[sort],
        ascending=False,
    )

    display_df = pd.DataFrame()

    display_df["Ticker"] = (
        terminal_df["symbol"]
        .str.replace(".NS", "", regex=False)
    )

    display_df["Company"] = terminal_df["company"]

    display_df["Sector"] = terminal_df["sector"]

    display_df["Price"] = terminal_df["price"].apply(
        lambda x: f"₹{x:,.2f}"
    )

    display_df["Change"] = terminal_df["Change"].apply(
        lambda x:
        f"🟢 {x:+.2f}%"
        if x >= 0
        else f"🔴 {x:+.2f}%"
    )

    display_df["P/E"] = (
        terminal_df["pe_ratio"]
        .round(2)
    )

    display_df["EPS"] = (
        terminal_df["eps"]
        .round(2)
    )

    display_df["Market Cap"] = terminal_df["market_cap"].apply(
        format_market_cap
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=520,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Companies",
            len(display_df),
        )

    with c2:
        st.metric(
            "Average Price",
            f"₹{terminal_df['price'].mean():,.2f}",
        )

    with c3:
        st.metric(
            "Average Change",
            f"{terminal_df['Change'].mean():+.2f}%"
        )

st.markdown(
    '<hr class="fp-section-gap">',
    unsafe_allow_html=True,
)
# =====================================================
# EQUITY WORKSPACE
# =====================================================

st.markdown(
    '<div class="panel-title">🏢 EQUITY WORKSPACE</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):

    st.caption(
        "Deep-dive into any tracked company with live financials, valuation, DNA analysis and historical price performance."
    )
    company_options = [
        f"{row.symbol.replace('.NS','')} — {row.company}"
        for _, row in df.iterrows()
    ]

    toolbar_col1, toolbar_col2 = st.columns([8, 3])

    with toolbar_col2:

        saved_col, button_col = st.columns([1, 2])

        with saved_col:

            st.markdown(
                f"""
                <div style="
                    background:#111827;
                    border:1px solid #1F2937;
                    border-radius:10px;
                    padding:8px 16px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    gap:8px;
                    height:42px;
                    margin-top:2px;
                ">
                    <span style="color:#9CA3AF; font-size:.82rem;">Saved</span>
                    <span style="color:#F9FAFB; font-weight:800; font-size:1rem;">{len(st.session_state.watchlist)}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    selected_company = st.selectbox(
        "",
        company_options,
        key="workspace_company",
        label_visibility="collapsed",
    )

    selected_symbol = selected_company.split(" — ")[0]

    selected_stock = df[
        df["symbol"].str.replace(".NS", "", regex=False)
        == selected_symbol
    ].iloc[0]

    in_watchlist = (
        selected_symbol in st.session_state.watchlist
    )

    with toolbar_col2:

        with button_col:

            if not in_watchlist:

                if st.button(
                    "⭐ Watchlist",
                    key="workspace_add",
                    use_container_width=True,
                ):

                    requests.post(f"{API_URL}/watchlist/{selected_symbol}")
                    st.session_state.watchlist.append(selected_symbol)
                    st.rerun()

            else:

                if st.button(
                    "🗑 Remove",
                    key="workspace_remove",
                    use_container_width=True,
                ):

                    requests.delete(f"{API_URL}/watchlist/{selected_symbol}")
                    st.session_state.watchlist.remove(selected_symbol)
                    st.rerun()

                    st.rerun()

    # -------------------------------------------------
    # WATCHLIST
    # -------------------------------------------------

    if st.session_state.watchlist:

        st.markdown("##### ⭐ Watchlist")

        chips = ""

        for company in st.session_state.watchlist:

            chips += f"""
            <span style="
                background:#111827;
                border:1px solid #1F2937;
                color:#E5E7EB;
                padding:8px 14px;
                border-radius:999px;
                margin-right:8px;
                margin-bottom:8px;
                display:inline-block;
                font-size:.9rem;
            ">
                {company}
            </span>
            """

        st.markdown(
            chips,
            unsafe_allow_html=True,
        )

    st.divider()

    # =====================================================
    # LOAD PRICE HISTORY
    # =====================================================

    try:

        response = requests.get(
            f"{API_URL}/history/{selected_stock['symbol']}"
        )

        response.raise_for_status()

        history_df = pd.DataFrame(
            response.json()
        )

        history_df["date"] = pd.to_datetime(
            history_df["date"]
        )

    except Exception:

        history_df = pd.DataFrame()

        st.warning(
            "Historical price data unavailable."
        )

    # =====================================================
    # WORKSPACE TABS
    # =====================================================

    snapshot_tab, financials_tab, dna_tab, chart_tab = st.tabs(
        [
            "📌 Snapshot",
            "💰 Financials",
            "🧬 DNA",
            "📈 Chart",
        ]
    )

# =====================================================
# SNAPSHOT
# =====================================================

with snapshot_tab:

    spotlight_card(selected_stock)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🤖 Explain this stock in 30 seconds", key="ai_summary_btn"):

        with st.spinner("Thinking..."):

            try:
                resp = requests.get(f"{API_URL}/ai-summary/{selected_stock['symbol']}")
                resp.raise_for_status()
                summary_text = resp.json()["summary"]

            except Exception:
                summary_text = "Couldn't generate a summary right now."

        st.session_state[f"ai_summary_{selected_stock['symbol']}"] = summary_text

    cached_summary = st.session_state.get(f"ai_summary_{selected_stock['symbol']}")

    if cached_summary:
        st.markdown(
            f"""
            <div style="
                background:#0F172A;
                border:1px solid rgba(34,197,94,.25);
                border-left:4px solid #22C55E;
                border-radius:12px;
                padding:18px 20px;
                margin-top:10px;
                color:#E5E7EB;
                font-size:.95rem;
                line-height:1.6;
            ">
            🤖 <b>AI Summary</b><br><br>{cached_summary}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Current Price",
            f"₹{selected_stock['price']:,.2f}",
        )

    with c2:

        st.metric(
            "P/E Ratio",
            f"{selected_stock['pe_ratio']:.2f}",
        )

    with c3:

        st.metric(
            "EPS",
            f"{selected_stock['eps']:.2f}",
        )

    with c4:

        st.metric(
            "Market Cap",
            format_market_cap(
                selected_stock["market_cap"]
            ),
        )

    st.divider()

    st.caption(
        "Snapshot generated from the latest available market data."
    )


# =====================================================
# FINANCIALS
# =====================================================

with financials_tab:

    display_key_financials(
        selected_stock["symbol"]
    )

    st.caption(
        "Financial statements are retrieved live from the backend and may vary between reporting periods."
    )

# =====================================================
# DNA
# =====================================================

with dna_tab:

    if history_df.empty:

        st.info(
            "No historical data available to generate FinPulse DNA."
        )

    else:

        dna = calculate_dna(
            selected_stock,
            history_df,
            df,
        )

        st.plotly_chart(
            create_dna_radar(dna),
            use_container_width=True,
            config={
                "displayModeBar": False
            },
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # -------------------------------------------------
        # DNA SCORES
        # -------------------------------------------------

        score1, score2, score3, score4, score5 = st.columns(5)

        metrics = [
            ("Growth", "🚀"),
            ("Value", "💎"),
            ("Stability", "🏛"),
            ("Momentum", "📈"),
            ("Risk", "⚠️"),
        ]

        columns = [
            score1,
            score2,
            score3,
            score4,
            score5,
        ]

        for (label, icon), column in zip(metrics, columns):

            with column:

                st.metric(
                    f"{icon} {label}",
                    f"{dna[label]}/100",
                )

        st.divider()

        # -------------------------------------------------
        # COMPANY ARCHETYPE
        # -------------------------------------------------

        if dna["Growth"] >= 80 and dna["Stability"] >= 80:

            archetype = "🏛 TITAN"

            description = (
                "Large-cap industry leader with excellent financial strength and dependable long-term performance."
            )

            colour = "#14532D"

        elif dna["Growth"] >= 80:

            archetype = "🚀 GROWTH ENGINE"

            description = (
                "High earnings potential with strong momentum, suitable for growth-focused investors."
            )

            colour = "#1E3A8A"

        elif dna["Value"] >= 80:

            archetype = "💎 VALUE GEM"

            description = (
                "Currently trading at an attractive valuation compared with peers."
            )

            colour = "#78350F"

        elif dna["Risk"] <= 30:

            archetype = "🛡 SAFE HAVEN"

            description = (
                "Historically stable with relatively low volatility and resilient price movement."
            )

            colour = "#166534"

        else:

            archetype = "⚡ EMERGING CHALLENGER"

            description = (
                "Balanced fundamentals with meaningful upside potential and room for future growth."
            )

            colour = "#3F3F46"

        st.markdown(
            f"""
<div style="
background:{colour};
padding:22px;
border-radius:14px;
border-left:5px solid #22C55E;
margin-bottom:20px;
">

<div style="
font-size:0.85rem;
letter-spacing:.12em;
text-transform:uppercase;
color:#CBD5E1;
">

Company Archetype

</div>

<div style="
font-size:1.7rem;
font-weight:800;
margin-top:10px;
margin-bottom:8px;
">

{archetype}

</div>

<div style="
font-size:.95rem;
color:#E5E7EB;
line-height:1.6;
">

{description}

</div>

</div>
""",
            unsafe_allow_html=True,
        )

        # -------------------------------------------------
        # DNA BREAKDOWN
        # -------------------------------------------------

        st.markdown(
            "#### 📋 DNA Breakdown"
        )

        explanations = {

            "Growth":
                "Reflects earnings strength relative to the rest of the market.",

            "Value":
                "Lower P/E companies receive higher value scores.",

            "Stability":
                "Derived from market capitalization and company size.",

            "Momentum":
                "Based on the relationship between the current price and the 20-day moving average.",

            "Risk":
                "Estimated from historical price volatility.",
        }

        for metric in [
            "Growth",
            "Value",
            "Stability",
            "Momentum",
            "Risk",
        ]:

            st.progress(
                dna[metric] / 100,
                text=f"{metric} • {dna[metric]}/100",
            )

            st.caption(
                explanations[metric]
            )

        st.info(
            "🧬 **FinPulse DNA** combines valuation, earnings, momentum, company size and historical volatility into a simplified profile for quick comparison."
        )

# =====================================================
# PRICE CHART
# =====================================================

with chart_tab:

    if history_df.empty:

        st.info(
            "Historical price data unavailable."
        )

    else:

        st.markdown(
            "#### 📈 Price History",
        )

        period = st.radio(
            "",
            [
                "1W",
                "1M",
                "3M",
                "6M",
                "1Y",
            ],
            horizontal=True,
            label_visibility="collapsed",
            key="history_period",
        )

        st.plotly_chart(
            create_price_chart(
                history_df,
                period,
            ),
            use_container_width=True,
            config={
                "displayModeBar": False,
            },
        )

        st.divider()

        # =====================================================
        # QUICK STATS
        # =====================================================

        latest = history_df.iloc[-1]

        highest = history_df["high"].max()
        lowest = history_df["low"].min()

        avg_volume = history_df["volume"].mean()

        returns = (
            (
                history_df["close"].iloc[-1]
                -
                history_df["close"].iloc[0]
            )
            /
            history_df["close"].iloc[0]
        ) * 100

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Latest Close",
                f"₹{latest['close']:,.2f}",
            )

        with c2:

            st.metric(
                "Highest Price",
                f"₹{highest:,.2f}",
            )

        with c3:

            st.metric(
                "Lowest Price",
                f"₹{lowest:,.2f}",
            )

        with c4:

            st.metric(
                "Return",
                f"{returns:+.2f}%",
            )

        st.divider()

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Average Volume",
                f"{avg_volume/1e6:.2f} M",
            )

        with c2:

            volatility = (
                history_df["close"]
                .pct_change()
                .std()
                * 100
            )

            st.metric(
                "Volatility",
                f"{volatility:.2f}%",
            )

        st.caption(
            "Statistics are calculated from the selected historical dataset."
        )

# =====================================================
# MARKET NEWS
# =====================================================

st.markdown(
    '<div class="panel-title">📰 MARKET NEWS</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):

    st.caption(
        "Latest business and market headlines from trusted financial news sources."
    )

    display_market_news()

st.markdown(
    '<hr class="fp-section-gap">',
    unsafe_allow_html=True,
)

# =====================================================
# PORTFOLIO SIMULATOR
# =====================================================

st.markdown(
    '<div class="panel-title">💼 PORTFOLIO SIMULATOR</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):

    st.caption(
        "Estimate your investment value, unrealized returns and portfolio performance using current market prices."
    )
    st.caption(
        "⚠️ Simulated for informational purposes only. Not real trading or investment advice."
    )

    c1, c2, c3 = st.columns([3, 2, 2])

    with c1:
        portfolio_symbol = st.selectbox(
            "Stock",
            df["symbol"].str.replace(".NS", "", regex=False),
            key="portfolio_stock",
        )

    portfolio_stock = df[
        df["symbol"].str.replace(".NS", "", regex=False)
        == portfolio_symbol
    ].iloc[0]

    with c2:
        shares = st.number_input(
            "Shares",
            min_value=1,
            value=25,
            step=1,
        )

    with c3:
        buy_price = st.number_input(
            "Buy Price (₹)",
            min_value=0.01,
            value=float(portfolio_stock["price"]),
            step=1.0,
        )

    portfolio = calculate_portfolio(
        portfolio_stock,
        shares,
        buy_price,
    )

    st.divider()

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "Investment",
            f"₹{portfolio['investment']:,.2f}",
        )

    with m2:
        st.metric(
            "Current Value",
            f"₹{portfolio['current_value']:,.2f}",
        )

    with m3:
        st.metric(
            "Profit / Loss",
            f"₹{portfolio['profit_loss']:,.2f}",
            f"{portfolio['return_percent']:+.2f}%",
        )

    if portfolio["profit_loss"] >= 0:
        st.success(
            f"Your investment is currently up by {portfolio['return_percent']:.2f}%."
        )
    else:
        st.error(
            f"Your investment is currently down by {abs(portfolio['return_percent']):.2f}%."
        )

st.markdown(
    '<hr class="fp-section-gap">',
    unsafe_allow_html=True,
)
# =====================================================
# MARKET ANALYTICS
# =====================================================

st.markdown(
    '<div class="panel-title">📊 MARKET ANALYTICS</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):

    st.caption(
        "Explore the overall market through valuation, capitalization and sector composition."
    )

    analytics_tab1, analytics_tab2, analytics_tab3 = st.tabs(
        [
            "🏦 Market Cap",
            "📐 P/E Ratio",
            "🧭 Sectors",
        ]
    )

    with analytics_tab1:

        st.plotly_chart(
            create_market_cap_chart(df),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with analytics_tab2:

        st.plotly_chart(
            create_pe_chart(df),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with analytics_tab3:

        st.plotly_chart(
            create_sector_chart(df),
            use_container_width=True,
            config={"displayModeBar": False},
        )

st.markdown(
    '<hr class="fp-section-gap">',
    unsafe_allow_html=True,
)

footer()