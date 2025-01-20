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
from app.services.yahoo_finance import fetch_data_from_yahoo_finance

def generate_hash(article: NewsArticleCreate) -> str:
    hash_data = f"{article.title}{article.published_date}{article.source}".encode()
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
                published_date = datetime.now(timezone.utc)
            description = item.find("description")
            if description is not None and description.text is not None:
                content = description.text.strip()
            else:
                content = "N/A"
            news_articles.append(NewsArticleCreate(title=title, source=source, published_date=published_date, content=content))
            print(f"Fetched article from PR Newswire: {title}")  # Debug statement
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
                published_date = datetime.now(timezone.utc)
            description = item.find("description")
            if description is not None and description.text is not None:
                content = description.text.strip()
            else:
                content = "N/A"
            news_articles.append(NewsArticleCreate(title=title, source=source, published_date=published_date, content=content))
            print(f"Fetched article from Business Wire: {title}")  # Debug statement
    else:
        print(f"Failed to fetch news from Business Wire: {response.status_code}")
    return news_articles

async def save_unique_news(db: Session, news_articles: List[NewsArticleCreate]):
    for article in news_articles:
        article_hash = generate_hash(article)
        if not db.query(NewsArticle).filter_by(hash=article_hash).first():
            db_article = NewsArticle(**article.dict(), hash=article_hash)
            db.add(db_article)
            print(f"Saving article: {article.title}")  # Debug statement
    try:
        db.commit()
        print("Committed news articles to the database.")  # Debug statement
    except Exception as e:
        db.rollback()
        print(f"Failed to commit news articles: {e}")

async def continuous_fetch():
    while True:
        try:
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
        except Exception as e:
            print(f"Error in continuous_fetch: {e}")
        await asyncio.sleep(3600)  # Fetch data every 10 minutes

def get_latest_news(db: Session, limit: int = 30) -> List[NewsArticle]:
    news_articles = db.query(NewsArticle).order_by(NewsArticle.published_date.desc()).limit(limit).all()
    print(f"Retrieved {len(news_articles)} articles from the database.")  # Debug statement
    return news_articles

def get_yahoo_finance_data() -> List[Dict[str, str]]:
    return fetch_data_from_yahoo_finance()
