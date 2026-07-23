from backend.database import SessionLocal
from backend.models import Stock

session = SessionLocal()

stocks = session.query(Stock).all()

for stock in stocks:
    print(
        stock.symbol,
        stock.company,
        stock.price,
        stock.pe_ratio
    )

session.close()