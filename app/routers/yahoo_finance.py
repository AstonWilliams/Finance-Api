from fastapi import APIRouter, Query
from typing import List, Dict
from app.services.yahoo_finance import fetch_data_from_yahoo_finance

router = APIRouter()

@router.get("/yahoofinance", response_model=List[Dict[str, str]])
def read_yahoo_finance_data(
    symbol: str = Query(None),
    name: str = Query(None),
    change: str = Query(None),
    change_percent: str = Query(None),
    price: str = Query(None),
    ytd_return: str = Query(None),
    three_mo_return: str = Query(None),
    one_year: str = Query(None),
    three_year_return: str = Query(None),
    five_year_return: str = Query(None),
    net_expense_ratio: str = Query(None),
    gross_expense_ratio: str = Query(None),
    net_assets: str = Query(None),
    fifty_day_avg: str = Query(None),
    two_hundred_day_avg: str = Query(None)
):
    data = fetch_data_from_yahoo_finance()
    query_params = {
        "Symbol": symbol,
        "Name": name,
        "Change": change,
        "Change %": change_percent,
        "Price (Intraday)": price,
        "YTD Return": ytd_return,
        "3-Mo Return": three_mo_return,
        "1-Year": one_year,
        "3-Year Return": three_year_return,
        "5-Year Return": five_year_return,
        "Net Expense Ratio": net_expense_ratio,
        "Gross Expense Ratio": gross_expense_ratio,
        "Net Assets": net_assets,
        "50 Day Avg": fifty_day_avg,
        "200 Day Avg": two_hundred_day_avg
    }
    filtered_data = [
        item for item in data
        if all(
            item.get(key) == value for key, value in query_params.items() if value is not None
        )
    ]

    return filtered_data
