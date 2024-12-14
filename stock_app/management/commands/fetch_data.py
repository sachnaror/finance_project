import yfinance as yf
from pymongo import MongoClient
from django.core.management.base import BaseCommand
from stock_app.models import StockData
from datetime import datetime

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017/")
mongo_db = client["finance_data"]
news_collection = mongo_db["news_articles"]

class Command(BaseCommand):
    help = "Fetch stock data and news articles for a given ticker"

    def add_arguments(self, parser):
        # Accept ticker symbols as command-line arguments
        parser.add_argument('tickers', nargs='+', type=str, help="Ticker symbols (e.g., MSFT AAPL GOOG)")

    def handle(self, *args, **options):
        tickers = options['tickers']
        for ticker in tickers:
            self.stdout.write(f"Fetching data for ticker: {ticker}")

            # Fetch stock history
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
            self.stdout.write(f"Stock data for {ticker} stored successfully!")

            # Fetch news articles (dummy data for now)
            articles = [{"title": f"News about {ticker}", "link": "http://example.com", "date": datetime.now()}]
            for article in articles:
                article["ticker"] = ticker
            news_collection.insert_many(articles)
            self.stdout.write(f"News for {ticker} stored successfully!")
