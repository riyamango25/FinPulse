from backend.database import engine, Base
from backend.models import Stock

Base.metadata.create_all(bind=engine)

print("Database and tables created successfully!")