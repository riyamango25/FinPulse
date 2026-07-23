from fastapi import FastAPI, HTTPException
from sqlalchemy import desc

from backend.ai_summary import get_ai_summary
from backend.database import SessionLocal, engine, Base
from backend.fetch_financials import get_financials
from backend.fetch_news import get_market_news
from backend.models import Stock, StockHistory, Watchlist

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinPulse API",
    description="Backend API for the FinPulse Stock Dashboard",
    version="2.0"
)


@app.get("/")
def home():
    return {"message": "Welcome to FinPulse API 🚀"}


# --------------------------------------------------
# All Stocks
# --------------------------------------------------
@app.get(
    "/stocks",
    summary="Get all stocks",
    description="Returns all stored Indian stocks."
)
def get_all_stocks():
    session = SessionLocal()

    try:
        stocks = session.query(Stock).all()

        return [
            {
                "symbol": stock.symbol,
                "company": stock.company,
                "sector": stock.sector,
                "price": stock.price,
                "prev_close": stock.prev_close,
                "market_cap": stock.market_cap,
                "pe_ratio": stock.pe_ratio,
                "eps": stock.eps,
                "day_high": stock.day_high,
                "day_low": stock.day_low,
                "volume": stock.volume
            }
            for stock in stocks
        ]

    finally:
        session.close()


# --------------------------------------------------
# Single Stock
# --------------------------------------------------
@app.get("/stocks/{symbol}")
def get_stock(symbol: str):
    session = SessionLocal()

    try:
        stock = session.query(Stock).filter(
            Stock.symbol == symbol
        ).first()

        if stock is None:
            raise HTTPException(
                status_code=404,
                detail="Stock not found"
            )

        return {
            "symbol": stock.symbol,
            "company": stock.company,
            "sector": stock.sector,
            "price": stock.price,
            "prev_close": stock.prev_close,
            "market_cap": stock.market_cap,
            "pe_ratio": stock.pe_ratio,
            "eps": stock.eps,
            "day_high": stock.day_high,
            "day_low": stock.day_low,
            "volume": stock.volume
        }

    finally:
        session.close()


# --------------------------------------------------
# Historical Prices
# --------------------------------------------------
@app.get("/history/{symbol}")
def get_history(symbol: str):
    session = SessionLocal()

    try:
        history = (
            session.query(StockHistory)
            .filter(StockHistory.symbol == symbol)
            .order_by(StockHistory.date)
            .all()
        )

        if not history:
            raise HTTPException(
                status_code=404,
                detail="No historical data found."
            )

        return [
            {
                "date": row.date.isoformat(),
                "open": row.open,
                "high": row.high,
                "low": row.low,
                "close": row.close,
                "volume": row.volume
            }
            for row in history
        ]

    finally:
        session.close()


# --------------------------------------------------
# Top PE Stocks
# --------------------------------------------------
@app.get("/top-pe")
def get_top_pe():
    session = SessionLocal()

    try:
        stocks = (
            session.query(Stock)
            .order_by(desc(Stock.pe_ratio))
            .limit(5)
            .all()
        )

        return [
            {
                "symbol": stock.symbol,
                "company": stock.company,
                "pe_ratio": stock.pe_ratio,
                "price": stock.price
            }
            for stock in stocks
        ]

    finally:
        session.close()


# --------------------------------------------------
# Financials
# --------------------------------------------------
@app.get("/financials/{symbol}")
def financials(symbol: str):

    data = get_financials(symbol)

    if "error" in data:
        raise HTTPException(
            status_code=500,
            detail=data["error"]
        )

    return data


# --------------------------------------------------
# Latest News
# --------------------------------------------------
@app.get("/market-news")
def market_news():
    return get_market_news()


# --------------------------------------------------
# Watchlist
# --------------------------------------------------
@app.get("/watchlist")
def get_watchlist():
    session = SessionLocal()

    try:
        items = session.query(Watchlist).all()
        return [item.symbol for item in items]

    finally:
        session.close()


@app.post("/watchlist/{symbol}")
def add_to_watchlist(symbol: str):
    session = SessionLocal()

    try:
        existing = session.query(Watchlist).filter(
            Watchlist.symbol == symbol
        ).first()

        if existing:
            return {"message": f"{symbol} already in watchlist"}

        entry = Watchlist(symbol=symbol)
        session.add(entry)
        session.commit()

        return {"message": f"{symbol} added to watchlist"}

    finally:
        session.close()


@app.delete("/watchlist/{symbol}")
def remove_from_watchlist(symbol: str):
    session = SessionLocal()

    try:
        entry = session.query(Watchlist).filter(
            Watchlist.symbol == symbol
        ).first()

        if not entry:
            raise HTTPException(status_code=404, detail="Symbol not in watchlist")

        session.delete(entry)
        session.commit()

        return {"message": f"{symbol} removed from watchlist"}

    finally:
        session.close()


# --------------------------------------------------
# AI Stock Summary
# --------------------------------------------------
@app.get("/ai-summary/{symbol}")
def ai_summary(symbol: str):
    session = SessionLocal()

    try:
        stock = session.query(Stock).filter(
            Stock.symbol == symbol
        ).first()

        if stock is None:
            raise HTTPException(status_code=404, detail="Stock not found")

        change = 0
        if stock.prev_close:
            change = ((stock.price - stock.prev_close) / stock.prev_close) * 100

        summary = get_ai_summary({
            "symbol": stock.symbol,
            "company": stock.company,
            "sector": stock.sector,
            "price": stock.price,
            "pe_ratio": stock.pe_ratio,
            "eps": stock.eps,
            "market_cap": stock.market_cap,
            "change": round(change, 2),
        })

        return {"summary": summary}

    finally:
        session.close()