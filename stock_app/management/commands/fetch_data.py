import yfinance as yf
from pymongo import MongoClient
from django.core.management.base import BaseCommand
from stock_app.models import StockData, NewsSource
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
mongo_db = client["finance_data"]
news_collection = mongo_db["news_articles"]

class Command(BaseCommand):
    help = "Fetch stock data and news articles"

    def fetch_news_links(self, ticker):
        """Fetch news articles dynamically for a ticker."""
        url = f"https://finance.yahoo.com/quote/{ticker}/news?p={ticker}"
        response = requests.get(url)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Failed to fetch news for {ticker}."))
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        news = []
        for item in soup.find_all("h3", class_="Mb(5px)"):
            try:
                link = "https://finance.yahoo.com" + item.a["href"]
                title = item.text.strip()
                news.append({"title": title, "link": link, "date": datetime.now()})
            except AttributeError:
                # Skip if structure is incorrect
                continue
        return news

    def handle(self, *args, **options):
        tickers = ["MSFT", "AAPL"]
        for ticker in tickers:
            try:
                self.stdout.write(f"Fetching stock data for {ticker}...")
                stock = yf.Ticker(ticker)
                history = stock.history(period="1mo")

                # Save to PostgreSQL
                for date, row in history.iterrows():
                    StockData.objects.update_or_create(
                        ticker=ticker,
                        date=date,
                        defaults={
                            "open": row["Open"],
                            "close": row["Close"],
                            "high": row["High"],
                            "low": row["Low"],
                            "volume": row["Volume"],
                        }
                    )
                self.stdout.write(self.style.SUCCESS(f"Stock data for {ticker} saved."))

                # Fetch and save news links
                news_articles = self.fetch_news_links(ticker)
                for article in news_articles:
                    # Save to MongoDB
                    article["ticker"] = ticker
                    if not news_collection.find_one({"link": article["link"]}):
                        news_collection.insert_one(article)

                    # Save to PostgreSQL (if needed)
                    NewsSource.objects.get_or_create(
                        ticker=ticker, link=article["link"]
                    )

                self.stdout.write(self.style.SUCCESS(f"News for {ticker} saved successfully."))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing {ticker}: {e}"))
