import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# =====================================================
# COMMON LAYOUT
# =====================================================

def apply_layout(fig, title):

    fig.update_layout(

        title=title,

        template="plotly_dark",

        paper_bgcolor="#0B0F19",
        plot_bgcolor="#0B0F19",

        font=dict(
            color="white",
            size=14,
        ),

        margin=dict(
            l=30,
            r=30,
            t=60,
            b=30,
        ),

        legend=dict(
            orientation="h",
            y=1.02,
            x=1,
            xanchor="right",
        ),

    )

    return fig


# =====================================================
# PRICE HISTORY
# =====================================================

def create_price_chart(history_df, period="1Y"):

    df = history_df.copy()

    if df.empty:
        return go.Figure()

    df["date"] = pd.to_datetime(df["date"])

    periods = {
        "1W": 7,
        "1M": 30,
        "3M": 90,
        "6M": 180,
    }

    if period in periods:
        df = df.tail(periods[period])

    df["MA20"] = df["close"].rolling(20).mean()

    fig = go.Figure()

    fig.add_trace(

        go.Candlestick(

            x=df["date"],

            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],

            name="Price",

            increasing_line_color="#22C55E",
            decreasing_line_color="#EF4444",

        )

    )

    fig.add_trace(

        go.Scatter(

            x=df["date"],
            y=df["MA20"],

            mode="lines",

            name="20 MA",

            line=dict(
                color="#60A5FA",
                width=2,
            ),

        )

    )

    fig.update_layout(

        height=320,

        hovermode="x unified",

        xaxis=dict(
            rangeslider=dict(
                visible=False,
            ),
            showgrid=False,
        ),

        yaxis=dict(
            title="Price (₹)",
            gridcolor="#1F2937",
        ),

    )

    return apply_layout(fig, "Price History")


# =====================================================
# MARKET CAP
# =====================================================

def create_market_cap_chart(df):

    top = (
        df.sort_values(
            "market_cap",
            ascending=False,
        )
        .head(10)
    )

    fig = px.bar(

        top,

        x=top["symbol"].str.replace(".NS", "", regex=False),

        y="market_cap",

        color="market_cap",

        text="market_cap",

    )

    fig.update_traces(

        texttemplate="%{y:.2s}",

        textposition="outside",

    )

    fig.update_layout(

        height=500,

        xaxis_title="Company",

        yaxis_title="Market Cap",

        coloraxis_showscale=False,

    )

    return apply_layout(fig, "Top Companies by Market Cap")


# =====================================================
# PE RATIO
# =====================================================

def create_pe_chart(df):

    top = (
        df.sort_values(
            "pe_ratio",
            ascending=False,
        )
        .head(10)
    )

    fig = px.line(

        top,

        x=top["symbol"].str.replace(".NS", "", regex=False),

        y="pe_ratio",

        markers=True,

    )

    fig.update_traces(

        line=dict(
            width=4,
            color="#22C55E",
        ),

        marker=dict(
            size=10,
        ),

    )

    fig.update_layout(

        height=500,

        xaxis_title="Company",

        yaxis_title="P/E Ratio",

    )

    return apply_layout(fig, "Highest P/E Ratios")


# =====================================================
# SECTOR ANALYSIS
# =====================================================

def create_sector_chart(df):

    sector = (
        df.groupby("sector", dropna=False)["market_cap"]
        .sum()
        .reset_index()
    )

    sector["sector"] = sector["sector"].fillna("Unknown")

    sector = sector.sort_values(
        "market_cap",
        ascending=True,
    )

    fig = px.bar(

        sector,

        x="market_cap",

        y="sector",

        orientation="h",

        color="market_cap",

        text="market_cap",

    )

    fig.update_traces(

        texttemplate="%{x:.2s}",

        textposition="outside",

    )

    fig.update_layout(

        height=520,

        margin=dict(
            l=40,
            r=100,
            t=50,
            b=40,
        ),

        xaxis_title="Market Cap",

        yaxis_title="",

        coloraxis_showscale=False,

    )

    return apply_layout(fig, "Sector Distribution")


# =====================================================
# PORTFOLIO
# =====================================================

def calculate_portfolio(stock, shares, purchase_price):

    current_price = float(stock["price"])

    investment = purchase_price * shares

    current_value = current_price * shares

    profit_loss = current_value - investment

    if investment == 0:

        return_percent = 0

    else:

        return_percent = (profit_loss / investment) * 100

    return {

        "investment": investment,

        "current_value": current_value,

        "profit_loss": profit_loss,

        "return_percent": return_percent,

    }


# =====================================================
# FINPULSE DNA
# =====================================================

def calculate_dna(stock, history_df, all_stocks):

    max_eps = max(float(all_stocks["eps"].max()), 1)

    growth = int(
        min(
            100,
            max(
                0,
                (float(stock["eps"]) / max_eps) * 100,
            ),
        )
    )

    value = int(
        min(
            100,
            max(
                0,
                100 - float(stock["pe_ratio"]) * 2,
            ),
        )
    )

    stability = int(

        min(

            100,

            max(

                0,

                (
                    float(stock["market_cap"])
                    / float(all_stocks["market_cap"].max())
                ) * 100,

            ),

        )

    )

    momentum = 50

    if len(history_df) >= 20:

        ma20 = history_df["close"].rolling(20).mean().iloc[-1]

        if pd.notna(ma20):

            momentum = int(

                min(

                    100,

                    max(

                        0,

                        (history_df["close"].iloc[-1] / ma20) * 50,

                    ),

                )

            )

    volatility = history_df["close"].pct_change().std()

    if pd.isna(volatility):

        volatility = 0

    risk = int(

        min(

            100,

            max(

                0,

                volatility * 1000,

            ),

        )

    )

    return {

        "Growth": growth,

        "Value": value,

        "Stability": stability,

        "Momentum": momentum,

        "Risk": risk,

    }