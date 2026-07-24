import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.fetch_financials import get_financials


# --------------------------------------------------
# Formatting Helpers
# --------------------------------------------------

def format_currency(value):

    if value is None:
        return "-"

    if value >= 1e12:
        return f"₹{value/1e12:.2f}T"

    if value >= 1e9:
        return f"₹{value/1e9:.2f}B"

    if value >= 1e6:
        return f"₹{value/1e6:.2f}M"

    return f"₹{value:,.0f}"


def format_percent(value):

    if value is None:
        return "-"

    return f"{value*100:.2f}%"


def format_number(value):

    if value is None:
        return "-"

    return f"{value:.2f}"


# --------------------------------------------------
# Card
# --------------------------------------------------

def financial_card(title, value):

    st.markdown(
        f"""
<div style="
background:#111827;
border:1px solid #1F2937;
border-radius:14px;
padding:14px;
margin-bottom:12px;
">

<div style="
font-size:12px;
color:#94A3B8;
text-transform:uppercase;
letter-spacing:1px;
">

{title}

</div>

<div style="
font-size:22px;
font-weight:700;
margin-top:6px;
">

{value}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# Main Component
# --------------------------------------------------

def display_key_financials(symbol):

    st.markdown(
        '<div class="panel-title">💰 KEY FINANCIALS</div>',
        unsafe_allow_html=True,
    )

    try:
        data = get_financials(symbol)
    except Exception:
        st.warning("Financial data unavailable.")
        return

    if not data or "error" in data:
        st.warning("Financial data unavailable.")
        return

    col1, col2 = st.columns(2)

    with col1:

        financial_card(
            "Revenue",
            format_currency(data.get("revenue")),
        )

        financial_card(
            "EPS",
            format_number(data.get("eps")),
        )

        financial_card(
            "Debt / Equity",
            format_number(data.get("debt_to_equity")),
        )

        financial_card(
            "Operating Margin",
            format_percent(
                data.get("operating_margin")
            ),
        )

    with col2:

        financial_card(
            "Net Income",
            format_currency(
                data.get("net_income")
            ),
        )

        financial_card(
            "ROE",
            format_percent(
                data.get("roe")
            ),
        )

        financial_card(
            "Current Ratio",
            format_number(
                data.get("current_ratio")
            ),
        )

        financial_card(
            "Dividend Yield",
            format_percent(
                data.get("dividend_yield")
            ),
        )