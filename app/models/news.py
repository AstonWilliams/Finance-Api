from sqlalchemy import Column, Integer, String, DateTime, Text
from app.db.database import Base

class NewsArticle(Base):
    __tablename__ = "news_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    source = Column(String, index=True)
    published_date = Column(DateTime)
    content = Column(Text)
    hash = Column(String, unique=True, index=True)

class YahooFinanceData(Base):
    __tablename__ = "yahoo_finance_data"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    name = Column(String, index=True)
    change = Column(String, nullable=True)
    change_percent = Column(String, nullable=True)
    price_intraday = Column(String, nullable=True)
    ytd_return = Column(String, nullable=True)
    three_mo_return = Column(String, nullable=True)
    one_year = Column(String, nullable=True)
    three_year_return = Column(String, nullable=True)
    five_year_return = Column(String, nullable=True)
    net_expense_ratio = Column(String, nullable=True)
    gross_expense_ratio = Column(String, nullable=True)
    net_assets = Column(String, nullable=True)
    fifty_day_avg = Column(String, nullable=True)
    two_hundred_day_avg = Column(String, nullable=True)
    hash = Column(String, unique=True, index=True)
