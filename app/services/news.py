import asyncio
import concurrent.futures
import requests
import hashlib
from datetime import datetime, timezone
from typing import List, Dict
from lxml import etree
from sqlalchemy.orm import Session
from app.models.news import NewsArticle
from app.schemas.news import NewsArticleCreate
from app.db.database import SessionLocal

def generate_hash(article: NewsArticleCreate) -> str:
    hash_data = article.title.encode()  # Use title for hash calculation
    return hashlib.sha256(hash_data).hexdigest()

def fetch_news_from_prnewswire() -> List[NewsArticleCreate]:
    url = "https://www.prnewswire.com/apac/rss/financial-services-latest-news/financial-services-latest-news-list.rss"
    response = requests.get(url)
    news_articles = []
    if response.status_code == 200:
        root = etree.fromstring(response.content)
        items = root.findall(".//item")
        for item in items:
            title = item.findtext("title", default="N/A")
            source = "PR Newswire"
            pub_date = item.findtext("pubDate", default="N/A")
            try:
                published_date = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
            except ValueError:
                published_date = datetime.now(timezone.utc)  # Fallback to current time if parsing fails
            content = item.findtext("description", default="N/A").strip()
            news_articles.append(NewsArticleCreate(title=title, source=source, published_date=published_date, content=content))
    else:
        print(f"Failed to fetch news from PR Newswire: {response.status_code}")
    return news_articles

def fetch_news_from_businesswire() -> List[NewsArticleCreate]:
    url = "https://feed.businesswire.com/rss/home/?rss=G1QFDERJXkJeGVtWXw==&_gl=1*1u452xi*_gcl_au*NTA5NzA4NDU3LjE3MzcwNTE0MzE.*_ga*MTk5NDgzNTI3MC4xNzM3MDUxNDMz*_ga_ZQWF70T3FK*MTczNzA1MTQzMi4xLjEuMTczNzA1MTQ2NC4yOC4wLjA."
    response = requests.get(url)
    news_articles = []
    if response.status_code == 200:
        root = etree.fromstring(response.content)
        items = root.findall(".//item")
        for item in items:
            title = item.findtext("title", default="N/A")
            source = "Business Wire"
            pub_date = item.findtext("pubDate", default="N/A")
            try:
                published_date = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
            except ValueError:
                published_date = datetime.now(timezone.utc)  # Fallback to current time if parsing fails
            content = item.findtext("description", default="N/A").strip()
            news_articles.append(NewsArticleCreate(title=title, source=source, published_date=published_date, content=content))
    else:
        print(f"Failed to fetch news from Business Wire: {response.status_code}")
    return news_articles

def fetch_data_from_yahoo_finance(start=0, count=100) -> List[Dict[str, str]]:
    if count not in [50, 100]:
        count = 100  # Default to 100 if an invalid count is provided
    base_url = "https://finance.yahoo.com/research-hub/screener/mutualfunds?start={start}&count={count}"
    data = []
    for i in range(0, 500, count):  # Adjust the range as needed
        url = base_url.format(start=i, count=count)
        response = requests.get(url)
        if response.status_code == 200:
            tree = etree.HTML(response.content)
            rows = tree.xpath("//tr[contains(@class, 'simpTblRow')]")  # Adjust XPath as needed
            for row in rows:
                data.append({
                    "Symbol": row.xpath(".//td[@aria-label='Symbol']/text()")[0].strip(),
                    "Name": row.xpath(".//td[@aria-label='Fund Name']//a/text()")[0].strip(),
                    "1D Chart": row.xpath(".//td[@aria-label='1D Chart']/text()")[0].strip(),
                    "Price (Intraday)": row.xpath(".//td[@aria-label='Price (Intraday)']/text()")[0].strip(),
                    "Change": row.xpath(".//td[@aria-label='Change']/text()")[0].strip(),
                    "Change %": row.xpath(".//td[@aria-label='Change %']/text()")[0].strip(),
                    "Volume": row.xpath(".//td[@aria-label='Volume']/text()")[0].strip(),
                    "YTD Return": row.xpath(".//td[@aria-label='YTD Return']/text()")[0].strip(),
                    "3-Mo Return": row.xpath(".//td[@aria-label='3-Mo Return']/text()")[0].strip(),
                    "1-Year": row.xpath(".//td[@aria-label='1-Year']/text()")[0].strip(),
                    "3-Year Return": row.xpath(".//td[@aria-label='3-Year Return']/text()")[0].strip(),
                    "5-Year Return": row.xpath(".//td[@aria-label='5-Year Return']/text()")[0].strip(),
                    "Net Expense Ratio": row.xpath(".//td[@aria-label='Net Expense Ratio']/text()")[0].strip(),
                    "Gross Expense Ratio": row.xpath(".//td[@aria-label='Gross Expense Ratio']/text()")[0].strip(),
                    "Net Assets": row.xpath(".//td[@aria-label='Net Assets']/text()")[0].strip(),
                    "Morningstar Rating": row.xpath(".//td[@aria-label='Morningstar Rating']/text()")[0].strip(),
                    "50 Day Avg": row.xpath(".//td[@aria-label='50 Day Avg']/text()")[0].strip(),
                    "200 Day Avg": row.xpath(".//td[@aria-label='200 Day Avg']/text()")[0].strip(),
                    "52 Week Range": row.xpath(".//td[@aria-label='52 Week Range']/text()")[0].strip()
                })
        else:
            print(f"Failed to fetch data from Yahoo Finance: {response.status_code}")
    return data

async def save_unique_news(db: Session, news_articles: List[NewsArticleCreate]):
    for article in news_articles:
        article_hash = generate_hash(article)
        if not db.query(NewsArticle).filter_by(hash=article_hash).first():
            db_article = NewsArticle(**article.dict(), hash=article_hash)
            db.add(db_article)
    db.commit()

async def continuous_fetch():
    while True:
        with SessionLocal() as db:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(fetch_news_from_prnewswire),
                    executor.submit(fetch_news_from_businesswire)
                ]
                news_articles = []
                for future in concurrent.futures.as_completed(futures):
                    news_articles.extend(future.result())

            # Sort news articles by published date, latest first
            news_articles.sort(key=lambda x: x.published_date, reverse=True)

            # Save unique articles to the database
            await save_unique_news(db, news_articles)
        await asyncio.sleep(600)  # Fetch data every 10 minutes

def get_latest_news(db: Session, limit: int = 8) -> List[NewsArticle]:
    return db.query(NewsArticle).order_by(NewsArticle.published_date.desc()).limit(limit).all()

def get_yahoo_finance_data() -> List[Dict[str, str]]:
    return fetch_data_from_yahoo_finance()
