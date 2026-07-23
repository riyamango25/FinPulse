import streamlit as st
from datetime import datetime


# =====================================================
# HEADER
# =====================================================

def header():

    now = datetime.now().strftime("%d %b %Y | %H:%M")

    left, right = st.columns([5, 1])

    with left:

        st.markdown(
            """
<div class="terminal-title">
FINPULSE TERMINAL<span class="cursor">_</span>
</div>

<div class="terminal-subtitle">
Indian Stock Intelligence Platform
</div>
""",
            unsafe_allow_html=True,
        )

    with right:

        st.metric(
            label="Status",
            value="🟢 LIVE",
            delta=now
        )

    st.divider()


# =====================================================
# COMPANY SNAPSHOT
# =====================================================

def spotlight_card(stock):

    st.markdown(
        '<div class="panel-title">COMPANY SNAPSHOT</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):

        st.subheader(stock["company"])

        st.caption(stock["symbol"].replace(".NS", ""))

        # ---------------------------------------
        # Price
        # ---------------------------------------

        price = stock["price"]
        prev = stock.get("prev_close") or price

        change = price - prev
        percent = (change / prev) * 100 if prev else 0

        if change >= 0:
            icon = "🟢"
            sign = "+"
        else:
            icon = "🔴"
            sign = ""

        st.markdown(f"## ₹{price:,.2f}")

        st.markdown(
            f"""
**{icon} {sign}{percent:.2f}% ({sign}₹{change:.2f}) Today**
"""
        )

        st.divider()

        # ---------------------------------------
        # Metrics
        # ---------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Market Cap",
                f"{stock['market_cap']/1e12:.2f} T"
            )

            st.metric(
                "EPS",
                f"{stock['eps']:.2f}"
            )

            st.metric(
                "Day High",
                f"₹{stock['day_high']:,.2f}"
            )

            st.metric(
                "Volume",
                f"{stock['volume']/1e6:.2f} M"
            )

        with col2:

            st.metric(
                "P/E Ratio",
                f"{stock['pe_ratio']:.2f}"
            )

            st.metric(
                "Sector",
                stock.get("sector", "N/A")
            )

            st.metric(
                "Day Low",
                f"₹{stock['day_low']:,.2f}"
            )

            st.metric(
                "Previous Close",
                f"₹{prev:,.2f}"
            )

        st.divider()

        # ---------------------------------------
        # Valuation
        # ---------------------------------------

        pe = stock["pe_ratio"] or 0

        if pe < 15:
            colour = "#22C55E"
            label = "🟢 UNDERVALUED"

        elif pe < 30:
            colour = "#FACC15"
            label = "🟡 FAIRLY VALUED"

        else:
            colour = "#EF4444"
            label = "🔴 OVERVALUED"

        st.markdown(
            f"""
            <div style="
                background:{colour};
                color:black;
                font-weight:700;
                text-align:center;
                padding:14px;
                border-radius:10px;
                font-size:16px;
                margin-top:12px;
                margin-bottom:8px;
            ">
                {label}
            </div>
            """,
            unsafe_allow_html=True,
        )


# =====================================================
# FOOTER
# =====================================================

def footer():

    st.markdown(
        """
<div style="
margin-top:60px;
padding:28px 20px;
border-top:1px solid #1F2937;
text-align:center;
color:#9CA3AF;
font-size:0.9rem;
line-height:1.8;
">

<div style="
font-size:1.05rem;
font-weight:700;
color:#F3F4F6;
margin-bottom:8px;
">
FINPULSE TERMINAL
</div>

<div>
Designed &amp; Developed by
<span style="color:#22C55E;font-weight:700;">Riya</span>
</div>

<div>
Electronics &amp; Instrumentation Engineering • BITS Pilani, K.K. Birla Goa Campus
</div>

<div>
Built with Python • Streamlit • FastAPI • Plotly • yFinance
</div>

<div style="
margin-top:14px;
color:#6B7280;
font-size:0.8rem;
">
© 2026 FinPulse Terminal · Academic Project
</div>

</div>
        """,
        unsafe_allow_html=True,
    )