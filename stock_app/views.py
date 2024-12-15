from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from .models import StockData
from datetime import datetime, timedelta
import yfinance as yf
import requests
from bs4 import BeautifulSoup

# MongoDB Configuration for News Articles
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["finance_data"]
news_collection = mongo_db["news_articles"]


def fetch_and_save_stock_data(ticker):
    """
    Fetch stock data using yfinance and save it to PostgreSQL.
    """
    # Check if data exists in PostgreSQL for the last 5 days
    last_5_days = datetime.now() - timedelta(days=5)
    existing_data = StockData.objects.filter(ticker=ticker.upper(), date__gte=last_5_days)

    if existing_data.exists():
        return list(existing_data.values())

    # Fetch new stock data using yfinance
    stock = yf.Ticker(ticker)
    history = stock.history(period="5d")

    if history.empty:
        return None

    stock_data = []
    for index, row in history.iterrows():
        stock_entry = StockData(
            ticker=ticker.upper(),
            date=index.date(),
            open_price=round(row["Open"], 2),
            high_price=round(row["High"], 2),
            low_price=round(row["Low"], 2),
            close_price=round(row["Close"], 2),
            volume=int(row["Volume"])
        )
        stock_data.append(stock_entry)

    # Save data to PostgreSQL
    StockData.objects.filter(ticker=ticker.upper()).delete()  # Remove old data
    StockData.objects.bulk_create(stock_data)

    return list(StockData.objects.filter(ticker=ticker.upper()).values())


def fetch_and_save_news(ticker):
    """
    Fetch top 5 news headlines by scraping Yahoo Finance and save to MongoDB.
    """
    existing_news = list(news_collection.find({"ticker": ticker.upper()}, {"_id": 0}))

    if existing_news:
        return existing_news

    url = f"https://finance.yahoo.com/quote/{ticker}/news"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    news_articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        news_blocks = soup.select("h3 a")[:5]
        for news in news_blocks:
            title = news.get_text(strip=True)
            link = news.get("href")
            if not link.startswith("https"):
                link = "https://finance.yahoo.com" + link
            news_articles.append({
                "ticker": ticker.upper(),
                "title": title,
                "link": link,
                "date": datetime.now().isoformat()
            })

    if news_articles:
        news_collection.delete_many({"ticker": ticker.upper()})
        news_collection.insert_many(news_articles)
    return news_articles


@api_view(["GET"])
def get_stock_data(request, ticker):
    """
    Fetch stock data from PostgreSQL or yfinance.
    """
    ticker = ticker.upper()
    stock_data = fetch_and_save_stock_data(ticker)

    if not stock_data:
        return Response({"message": f"No stock data available for {ticker}."})

    return Response({"ticker": ticker, "data": stock_data})


@api_view(["GET"])
def get_news_articles(request, ticker):
    """
    Fetch news articles from MongoDB or Yahoo Finance.
    """
    ticker = ticker.upper()
    news_data = fetch_and_save_news(ticker)

    if not news_data:
        return Response({"message": f"No news articles found for {ticker}."})

    return Response({"ticker": ticker, "news": news_data})
