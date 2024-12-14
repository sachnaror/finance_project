import yfinance as yf
import pandas as pd
from pymongo import MongoClient
from django.core.management.base import BaseCommand
from stock_app.models import StockData, NewsSource
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017/")
mongo_db = client["finance_data"]
news_collection = mongo_db["news_articles"]

class Command(BaseCommand):
    help = "Fetch stock data and news articles"

    def fetch_news_links(self, ticker):
        """Fetch news articles dynamically for a ticker."""
        url = f"https://finance.yahoo.com/quote/{ticker}/news?p={ticker}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        news = []
        for item in soup.find_all("h3", class_="Mb(5px)"):
            link = "https://finance.yahoo.com" + item.a["href"]
            title = item.text
            news.append({"title": title, "link": link, "date": datetime.now()})
        return news

    def handle(self, *args, **options):
        # Fetch stock data
        tickers = ["MSFT", "AAPL"]
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            history = stock.history(period="1mo")

            for date, row in history.iterrows():
                StockData.objects.create(
                    ticker=ticker,
                    date=date,
                    open=row["Open"],
                    close=row["Close"],
                    high=row["High"],
                    low=row["Low"],
                    volume=row["Volume"]
                )
            self.stdout.write(f"Stock data for {ticker} fetched successfully!")

            # Fetch and save news links dynamically
            news_articles = self.fetch_news_links(ticker)
            for article in news_articles:
                # Save to MongoDB
                article["ticker"] = ticker
                news_collection.insert_one(article)

                # Save to PostgreSQL (Optional: Save the news source)
                NewsSource.objects.get_or_create(
                    ticker=ticker,
                    link=article["link"]
                )
            self.stdout.write(f"News for {ticker} stored successfully.")
