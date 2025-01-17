import requests
import hashlib
from typing import List, Dict
from lxml import html
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.news import YahooFinanceData
import asyncio

base_url = "https://finance.yahoo.com/research-hub/screener/mutualfunds?start={start}&count={count}"

desired_columns = [
    "Symbol", "Name", "1D Chart", "Price (Intraday)", "Change", "Change %",
    "Volume", "YTD Return", "3-Mo Return", "1-Year", "3-Year Return", "5-Year Return",
    "Net Expense Ratio", "Gross Expense Ratio", "Net Assets", "Morningstar Rating",
    "50 Day Avg", "200 Day Avg", "52 Week Range"
]

def generate_hash(data: Dict[str, str]) -> str:
    hash_data = (data["Symbol"] + data["Name"] + data["Price (Intraday)"]).encode()
    return hashlib.sha256(hash_data).hexdigest()

def fetch_and_store_data_from_yahoo_finance(start=0, count=100):
    session: Session = SessionLocal()
    url = base_url.format(start=start, count=count)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        rows = tree.xpath("//tr[contains(@class, 'simpTblRow')]")
        
        for row in rows:
            cells = row.xpath(".//td")
            if len(cells) == len(desired_columns):
                row_data = {col: cells[i].text_content().strip() for i, col in enumerate(desired_columns)}
                row_data_hash = generate_hash(row_data)

                # Hashing to remove duplicates
                existing_record = session.query(YahooFinanceData).filter_by(hash=row_data_hash).first()
                if not existing_record:
                    new_record = YahooFinanceData(
                        symbol=row_data["Symbol"],
                        name=row_data["Name"],
                        chart=row_data["1D Chart"],
                        price_intraday=row_data["Price (Intraday)"],
                        change=row_data["Change"],
                        change_percent=row_data["Change %"],
                        volume=row_data["Volume"],
                        ytd_return=row_data["YTD Return"],
                        three_mo_return=row_data["3-Mo Return"],
                        one_year=row_data["1-Year"],
                        three_year_return=row_data["3-Year Return"],
                        five_year_return=row_data["5-Year Return"],
                        net_expense_ratio=row_data["Net Expense Ratio"],
                        gross_expense_ratio=row_data["Gross Expense Ratio"],
                        net_assets=row_data["Net Assets"],
                        morningstar_rating=row_data["Morningstar Rating"],
                        fifty_day_avg=row_data["50 Day Avg"],
                        two_hundred_day_avg=row_data["200 Day Avg"],
                        fifty_two_week_range=row_data["52 Week Range"],
                        hash=row_data_hash
                    )
                    session.add(new_record)
                    session.commit()
    else:
        print(f"Failed to fetch data from Yahoo Finance: {response.status_code}")
    session.close()

async def continuous_yahoo_finance_fetch():
    while True:
        fetch_and_store_data_from_yahoo_finance(start=0, count=100)
        await asyncio.sleep(20)  # Fetch data every 20 seconds

def fetch_data_from_yahoo_finance(start=0, count=100) -> List[Dict[str, str]]:
    url = base_url.format(start=start, count=count)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    data = []
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        rows = tree.xpath("//tr[contains(@class, 'simpTblRow')]")
        
        for row in rows:
            cells = row.xpath(".//td")
            if len(cells) == len(desired_columns):
                row_data = {col: cells[i].text_content().strip() for i, col in enumerate(desired_columns)}
                data.append(row_data)
    else:
        print(f"Failed to fetch data from Yahoo Finance: {response.status_code}")
    return data
