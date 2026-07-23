import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"


# =====================================================
# MARKET NEWS
# =====================================================

def display_market_news():

    try:

        response = requests.get(
            f"{API_URL}/market-news"
        )

        response.raise_for_status()

        articles = response.json()

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
">

<a
href="{link}"
target="_blank"
style="
text-decoration:none;
color:white;
">

{title}

</a>

</div>

<div style="
font-size:13px;
font-weight:600;
color:#22C55E;
">

Read Full Story →

</div>

</div>
""",
            unsafe_allow_html=True,
        )