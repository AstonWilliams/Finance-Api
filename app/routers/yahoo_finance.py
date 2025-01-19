from fastapi import APIRouter, Query
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.news import YahooFinanceData

router = APIRouter()

@router.get("/yahoofinance", response_model=List[Dict[str, str]])
async def read_yahoo_finance_data(
    symbol: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    change: Optional[str] = Query(None),
    change_percent: Optional[str] = Query(None),
    price: Optional[str] = Query(None),
    ytd_return: Optional[str] = Query(None),
    three_mo_return: Optional[str] = Query(None),
    one_year: Optional[str] = Query(None),
    three_year_return: Optional[str] = Query(None),
    five_year_return: Optional[str] = Query(None),
    net_expense_ratio: Optional[str] = Query(None),
    gross_expense_ratio: Optional[str] = Query(None),
    net_assets: Optional[str] = Query(None),
    fifty_day_avg: Optional[str] = Query(None),
    two_hundred_day_avg: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None),
    sort_order: Optional[str] = Query("asc")
):
    session: Session = SessionLocal()
    query = session.query(YahooFinanceData)
    
    if symbol:
        query = query.filter(YahooFinanceData.symbol == symbol)
    if name:
        query = query.filter(YahooFinanceData.name == name)
    if change:
        query = query.filter(YahooFinanceData.change == change)
    if change_percent:
        query = query.filter(YahooFinanceData.change_percent == change_percent)
    if price:
        query = query.filter(YahooFinanceData.price_intraday == price)
    if ytd_return:
        query = query.filter(YahooFinanceData.ytd_return == ytd_return)
    if three_mo_return:
        query = query.filter(YahooFinanceData.three_mo_return == three_mo_return)
    if one_year:
        query = query.filter(YahooFinanceData.one_year == one_year)
    if three_year_return:
        query = query.filter(YahooFinanceData.three_year_return == three_year_return)
    if five_year_return:
        query = query.filter(YahooFinanceData.five_year_return == five_year_return)
    if net_expense_ratio:
        query = query.filter(YahooFinanceData.net_expense_ratio == net_expense_ratio)
    if gross_expense_ratio:
        query = query.filter(YahooFinanceData.gross_expense_ratio == gross_expense_ratio)
    if net_assets:
        query = query.filter(YahooFinanceData.net_assets == net_assets)
    if fifty_day_avg:
        query = query.filter(YahooFinanceData.fifty_day_avg == fifty_day_avg)
    if two_hundred_day_avg:
        query = query.filter(YahooFinanceData.two_hundred_day_avg == two_hundred_day_avg)

    if sort_by:
        if sort_order == "desc":
            query = query.order_by(getattr(YahooFinanceData, sort_by).desc())
        else:
            query = query.order_by(getattr(YahooFinanceData, sort_by).asc())

    result = query.all()
    session.close()

    # Convert SQLAlchemy objects to dictionaries
    result_data = [
        {
            "Symbol": record.symbol,
            "Name": record.name,
            "Price (Intraday)": record.price_intraday,
            "Change": record.change,
            "Change %": record.change_percent,
            "Volume": record.volume,
            "YTD Return": record.ytd_return,
            "3-Mo Return": record.three_mo_return,
            "1-Year": record.one_year,
            "3-Year Return": record.three_year_return,
            "5-Year Return": record.five_year_return,
            "Net Expense Ratio": record.net_expense_ratio,
            "Gross Expense Ratio": record.gross_expense_ratio,
            "Net Assets": record.net_assets,
            "Morningstar Rating": record.morningstar_rating,
            "50 Day Avg": record.fifty_day_avg,
            "200 Day Avg": record.two_hundred_day_avg,
            "timestamp": record.timestamp.isoformat()  # Ensure timestamp is a string
        }
    for record in result]

    return result_data
