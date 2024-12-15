from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from datetime import datetime
import yfinance as yf
import requests
from bs4 import BeautifulSoup

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017/")
news_db = client["finance_data"]
news_collection = news_db["news_articles"]



def fetch_top_news(ticker):
    """
    Fetch top 5 latest press releases or news articles for a given ticker using Yahoo Finance's hidden JSON API.
    """
    url = f"https://query1.finance.yahoo.com/v1/finance/search?q={ticker}&newsCount=5"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    news_articles = []

    print("Response Status Code:", response.status_code)

    if response.status_code == 200:
        data = response.json()

        # Extract the top 5 news articles
        for article in data.get("news", [])[:5]:
            title = article.get("title", "No title")
            link = article.get("link", "https://finance.yahoo.com")
            date = datetime.fromtimestamp(article.get("providerPublishTime", datetime.now().timestamp()))

            news_articles.append({
                "title": title,
                "link": link,
                "date": date.isoformat(),
                "ticker": ticker.upper()
            })

    else:
        print(f"Error fetching data from Yahoo Finance API: HTTP {response.status_code}")

    return news_articles

@api_view(["GET"])
def get_news_articles(request, ticker):
    """
    Fetch and return top 5 latest news articles for a given ticker.
    """
    ticker = ticker.upper()

    # Check MongoDB for saved news
    news = list(news_collection.find({"ticker": ticker}, {"_id": 0}))

    if news:
        return Response(news)

    # Fetch live news if no saved data exists
    live_news = fetch_top_news(ticker)

    if live_news:
        # Delete old news for the ticker to avoid duplicates
        news_collection.delete_many({"ticker": ticker})
        # Save the new top 5 news headlines to MongoDB
        news_collection.insert_many(live_news)
        return Response(live_news)

    return Response({"message": f"No news articles found for {ticker}."})


@api_view(["GET"])
def get_stock_data(request, ticker):
    """
    Fetch stock data for the given ticker using yfinance.
    """
    ticker = ticker.upper()
    stock = yf.Ticker(ticker)

    try:
        # Fetch last 5 days of stock data
        history = stock.history(period="5d")
        data = [
            {
                "date": index.strftime("%Y-%m-%d"),
                "open": round(row["Open"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2),
                "close": round(row["Close"], 2),
                "volume": int(row["Volume"])
            }
            for index, row in history.iterrows()
        ]
        return Response({"ticker": ticker, "data": data})
    except Exception as e:
        return Response({"message": "Failed to fetch stock data.", "error": str(e)})
