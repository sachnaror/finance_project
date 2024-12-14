from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017/")
news_db = client["finance_data"]  # Database name
news_collection = news_db["news_articles"]  # Collection name

def fetch_live_news(ticker):
    """
    Fetch top 5 latest news headlines for the given ticker symbol by scraping Yahoo Finance.
    """
    url = f"https://finance.yahoo.com/quote/{ticker}/news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    news_articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Yahoo Finance News Selector: Adjusted for the latest structure
        headlines = soup.select('li.js-stream-content h3 a')[:5]  # Select the top 5 headlines

        for headline in headlines:
            title = headline.get_text(strip=True)
            link = headline["href"]

            # Ensure full link URL
            if not link.startswith("https"):
                link = "https://finance.yahoo.com" + link

            news_articles.append({
                "title": title,
                "link": link,
                "date": datetime.now().isoformat(),
                "ticker": ticker.upper()
            })

    else:
        print(f"Error fetching data from Yahoo Finance: {response.status_code}")

    return news_articles


@api_view(["GET"])
def get_news_articles(request, ticker):
    """
    API View to fetch and return top 5 latest news articles for a given ticker symbol.
    - Checks MongoDB for saved articles.
    - If no articles exist, fetch live data, save it, and return.
    """
    ticker = ticker.upper()

    # Check MongoDB for saved news
    news = list(news_collection.find({"ticker": ticker}, {"_id": 0}))

    if news:
        # If news exists in MongoDB, return it
        return Response(news)

    # Fetch live news if no saved data exists
    live_news = fetch_live_news(ticker)

    if live_news:
        # Delete old news for the ticker to avoid duplicates
        news_collection.delete_many({"ticker": ticker})
        # Save the new top 5 news headlines to MongoDB
        news_collection.insert_many(live_news)
        return Response(live_news)

    # Return message if no news found
    return Response({"message": f"No news articles found for {ticker}."})


@api_view(["GET"])
def get_stock_data(request, ticker):
    """
    API View to fetch and return stock data for a given ticker symbol.
    This is currently a placeholder and can be connected to yfinance or another API.
    """
    # Placeholder response for stock data
    data = {
        "ticker": ticker.upper(),
        "message": "Stock data endpoint placeholder. Connect to a stock API like Yahoo Finance."
    }
    return Response(data)
