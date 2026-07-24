import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.fetch_news import get_market_news


# =====================================================
# MARKET NEWS
# =====================================================

def display_market_news():

    try:
        articles = get_market_news()
    except Exception:
        st.warning("Unable to load market news.")
        return

    if not articles:
        st.info("No recent news available.")
        return

    for article in articles:

        title = article.get("title", "Untitled")
        publisher = article.get("publisher", "Unknown")
        published = article.get("published", "")
        link = article.get("link", "")

        st.markdown(
            f"""
<a href="{link}" target="_blank" style="text-decoration:none;color:inherit;display:block;">
<div style="
background:#111827;
border:1px solid #1F2937;
border-left:4px solid #22C55E;
border-radius:12px;
padding:16px 18px;
margin-bottom:12px;
transition:.2s;
">

<div style="
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:10px;
">

<div style="
font-size:12px;
letter-spacing:.12em;
text-transform:uppercase;
color:#94A3B8;
">

{publisher}

</div>

<div style="
font-size:12px;
color:#6B7280;
">

{published}

</div>

</div>

<div style="
font-size:18px;
font-weight:700;
line-height:1.45;
margin-bottom:14px;
color:white;
">

{title}

</div>

<div style="
font-size:13px;
font-weight:600;
color:#22C55E;
">

Read Full Story →

</div>

</div>
</a>
""",
            unsafe_allow_html=True,
        )