from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.services.news import get_latest_news
from app.services.yahoo_finance import fetch_data_from_yahoo_finance, fetch_and_store_data_from_yahoo_finance
from app.db.database import get_db
from app.schemas.news import NewsArticle, HTTPValidationError
from typing import List, Dict

router = APIRouter()

@router.get("/news", response_model=List[NewsArticle], responses={422: {"model": HTTPValidationError}})
def read_news(db: Session = Depends(get_db)):
    news = get_latest_news(db)
    return news

@router.get("/yahoofinance", response_model=List[Dict[str, str]], responses={422: {"model": HTTPValidationError}})
def read_yahoo_finance_data(
    start: int = 0,
    count: int = 100,
    symbol: str = Query(None),
    name: str = Query(None),
    chart: str = Query(None),
    price: str = Query(None),
    change: str = Query(None),
    change_percent: str = Query(None),
    volume: str = Query(None),
    ytd_return: str = Query(None),
    three_mo_return: str = Query(None),
    one_year: str = Query(None),
    three_year_return: str = Query(None),
    five_year_return: str = Query(None),
    net_expense_ratio: str = Query(None),
    gross_expense_ratio: str = Query(None),
    net_assets: str = Query(None),
    morningstar_rating: str = Query(None),
    fifty_day_avg: str = Query(None),
    two_hundred_day_avg: str = Query(None),
    fifty_two_week_range: str = Query(None)
):
    data = fetch_data_from_yahoo_finance(start=start, count=count)
    fetch_and_store_data_from_yahoo_finance(start=start, count=count)
    query_params = {
        "Symbol": symbol,
        "Name": name,
        "1D Chart": chart,
        "Price (Intraday)": price,
        "Change": change,
        "Change %": change_percent,
        "Volume": volume,
        "YTD Return": ytd_return,
        "3-Mo Return": three_mo_return,
        "1-Year": one_year,
        "3-Year Return": three_year_return,
        "5-Year Return": five_year_return,
        "Net Expense Ratio": net_expense_ratio,
        "Gross Expense Ratio": gross_expense_ratio,
        "Net Assets": net_assets,
        "Morningstar Rating": morningstar_rating,
        "50 Day Avg": fifty_day_avg,
        "200 Day Avg": two_hundred_day_avg,
        "52 Week Range": fifty_two_week_range
    }

    filtered_data = [
        item for item in data
        if all(
            item.get(key) == value for key, value in query_params.items() if value is not None
        )
    ]

    return filtered_data
