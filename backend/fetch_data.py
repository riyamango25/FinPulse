import yfinance as yf

from backend.database import SessionLocal
from backend.models import Stock, StockHistory

# ----------------------------
# Database Session
# ----------------------------
session = SessionLocal()

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "LT.NS",
    "ITC.NS",
    "BHARTIARTL.NS",
    "MARUTI.NS",
    "AXISBANK.NS",
    "SUNPHARMA.NS",
    "TITAN.NS",
    "BAJFINANCE.NS",
    "NESTLEIND.NS",
    "ULTRACEMCO.NS",
    "ASIANPAINT.NS",
    "WIPRO.NS",
    "KOTAKBANK.NS",
    "HINDUNILVR.NS",
]

for symbol in stocks:
    print(f"Fetching {symbol}...")

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        # ----------------------------
        # Current Stock Snapshot
        # ----------------------------
        stock = Stock(
            symbol=symbol,
            company=info.get("longName"),
            sector=info.get("sector"),
            price=info.get("currentPrice"),
            prev_close=info.get("previousClose"),
            market_cap=info.get("marketCap"),
            pe_ratio=info.get("trailingPE"),
            eps=info.get("trailingEps"),
            day_high=info.get("dayHigh"),
            day_low=info.get("dayLow"),
            volume=info.get("volume"),
        )

        session.merge(stock)
        session.commit()

        # ----------------------------
        # Remove Existing History
        # ----------------------------
        session.query(StockHistory).filter(
            StockHistory.symbol == symbol
        ).delete()

        session.commit()

        # ----------------------------
        # Download 1 Year History
        # ----------------------------
        history = ticker.history(period="1y", interval="1d")

        for date, row in history.iterrows():
            history_row = StockHistory(
                symbol=symbol,
                date=date.date(),
                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),
                volume=int(row["Volume"]),
            )

            session.add(history_row)

        session.commit()

        print(f"✅ {symbol} updated.")

    except Exception as e:
        session.rollback()
        print(f"❌ Failed for {symbol}: {e}")

session.close()

print("\n🎉 Database successfully updated!")