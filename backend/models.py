from sqlalchemy import Column, String, Float, BigInteger, Integer, Date, ForeignKey
from backend.database import Base


class Stock(Base):
    """Current snapshot of a stock's price and fundamentals."""
    __tablename__ = "stocks"

    symbol = Column(String, primary_key=True)
    company = Column(String)
    sector = Column(String)
    price = Column(Float)
    prev_close = Column(Float)
    market_cap = Column(BigInteger)
    pe_ratio = Column(Float)
    eps = Column(Float)
    day_high = Column(Float)
    day_low = Column(Float)
    volume = Column(BigInteger)


class StockHistory(Base):
    """Historical daily OHLCV data, used to power the price charts."""
    __tablename__ = "stock_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String, ForeignKey("stocks.symbol"), index=True)
    date = Column(Date, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)

class Watchlist(Base):
    """Stocks saved by the user to their watchlist."""
    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String, ForeignKey("stocks.symbol"), unique=True, index=True)