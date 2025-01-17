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
    "Symbol", "Name", "Price (Intraday)", "Change", "Change %",
    "Volume", "YTD Return", "3-Mo Return", "1-Year", "3-Year Return", "5-Year Return",
    "Net Expense Ratio", "Gross Expense Ratio", "Net Assets", "Morningstar Rating",
    "50 Day Avg", "200 Day Avg", "52 Week Range"
]

def generate_hash(data: Dict[str, str]) -> str:
    hash_data = "".join([data[column] for column in desired_columns if column in data]).encode()
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
        rows = tree.xpath("//tr[contains(@class, 'row yf-11hlglb')]")
        
        for row in rows:
            cells = row.xpath(".//td")
            if len(cells) >= len(desired_columns):
                row_data = {
                    "Symbol": cells[0].text_content().strip(),
                    "Name": cells[1].text_content().strip(),
                    "Price (Intraday)": cells[2].text_content().strip(),
                    "Change": cells[3].text_content().strip(),
                    "Change %": cells[4].text_content().strip(),
                    "Volume": cells[5].text_content().strip(),
                    "YTD Return": cells[6].text_content().strip(),
                    "3-Mo Return": cells[7].text_content().strip(),
                    "1-Year": cells[8].text_content().strip(),
                    "3-Year Return": cells[9].text_content().strip(),
                    "5-Year Return": cells[10].text_content().strip(),
                    "Net Expense Ratio": cells[11].text_content().strip(),
                    "Gross Expense Ratio": cells[12].text_content().strip(),
                    "Net Assets": cells[13].text_content().strip(),
                    "Morningstar Rating": cells[14].text_content().strip(),
                    "50 Day Avg": cells[15].text_content().strip(),
                    "200 Day Avg": cells[16].text_content().strip(),
                    "52 Week Range": cells[17].text_content().strip()
                }
                row_data_hash = generate_hash(row_data)

                # Check for duplicates
                existing_record = session.query(YahooFinanceData).filter_by(hash=row_data_hash).first()
                if not existing_record:
                    new_record = YahooFinanceData(
                        symbol=row_data["Symbol"],
                        name=row_data["Name"],
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
        rows = tree.xpath("//tr[contains(@class, 'row yf-11hlglb')]")
        
        for row in rows:
            cells = row.xpath(".//td")
            if len(cells) >= len(desired_columns):
                row_data = {
                    "Symbol": cells[0].text_content().strip(),
                    "Name": cells[1].text_content().strip(),
                    "Price (Intraday)": cells[2].text_content().strip(),
                    "Change": cells[3].text_content().strip(),
                    "Change %": cells[4].text_content().strip(),
                    "Volume": cells[5].text_content().strip(),
                    "YTD Return": cells[6].text_content().strip(),
                    "3-Mo Return": cells[7].text_content().strip(),
                    "1-Year": cells[8].text_content().strip(),
                    "3-Year Return": cells[9].text_content().strip(),
                    "5-Year Return": cells[10].text_content().strip(),
                    "Net Expense Ratio": cells[11].text_content().strip(),
                    "Gross Expense Ratio": cells[12].text_content().strip(),
                    "Net Assets": cells[13].text_content().strip(),
                    "Morningstar Rating": cells[14].text_content().strip(),
                    "50 Day Avg": cells[15].text_content().strip(),
                    "200 Day Avg": cells[16].text_content().strip(),
                    "52 Week Range": cells[17].text_content().strip()
                }
                data.append(row_data)
    else:
        print(f"Failed to fetch data from Yahoo Finance: {response.status_code}")
    return data
