from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from django.utils.timezone import now
from .models import StockData
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
import time

# MongoDB Configuration
mongo_client = MongoClient("mongodb://localhost:27017/")
news_collection = mongo_client["finance_data"]["news_articles"]

# Proxy Configuration
PROXY_URL = "http://mark:jsCADlew3zjOC@proxy.monalisa.io:31112" #This proxy had limited credits and seems to havhe been consumed while testing this.
CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver"

# User Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
]


# Safe Page Loading for Selenium
def safe_get(driver, url, retries=3):
    for attempt in range(retries):
        try:
            driver.get(url)
            return True
        except Exception as e:
            print(f"Error loading page: {e}, retrying ({attempt + 1}/{retries})...")
            time.sleep(2)
    return False






def fetch_and_save_news(ticker):
    """
    Fetch top 5-10 latest news headlines for the given ticker symbol using Selenium and Yahoo Finance.
    """
    url = f"https://finance.yahoo.com/quote/{ticker}/news"

    # Configure Selenium ChromeDriver without Proxy for Debugging
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920x1080")
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    # options.add_argument(f"--proxy-server={PROXY_URL}")  # Temporarily disabled

    service = Service(CHROME_DRIVER_PATH)
    driver = None

    news_articles = []

    try:
        driver = webdriver.Chrome(service=service, options=options)

        # Safe get with retries
        if not safe_get(driver, url):
            print("Failed to load the page after retries.")
            return [{"message": f"Failed to fetch news for {ticker}."}]

        # Wait for page content to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.js-stream-content"))
        )
        time.sleep(5)  # Allow time for AJAX content to load

        # Debug: Print page source
        print("Page Source Length:", len(driver.page_source))
        print("Full Page Source:\n", driver.page_source[:2000])

        soup = BeautifulSoup(driver.page_source, "html.parser")
        news_blocks = soup.select("li.js-stream-content")
        print(f"Found {len(news_blocks)} news blocks")

        for block in news_blocks[:10]:
            try:
                title_tag = block.find("h3")
                link_tag = block.find("a", href=True)

                if title_tag and link_tag:
                    title = title_tag.get_text(strip=True)
                    link = link_tag["href"]
                    if not link.startswith("https"):
                        link = "https://finance.yahoo.com" + link

                    time_tag = block.find("time")
                    date = time_tag["datetime"] if time_tag else datetime.now().isoformat()

                    news_articles.append({
                        "ticker": ticker.upper(),
                        "title": title,
                        "link": link,
                        "date": date
                    })
            except Exception as e:
                print(f"Error parsing news block: {e}")
    except Exception as e:
        print(f"Error loading or processing page: {e}")
    finally:
        if driver:
            driver.quit()

    # Save news to MongoDB
    if news_articles:
        news_collection.delete_many({"ticker": ticker.upper()})
        news_collection.insert_many(news_articles)
        print(f"Saved {len(news_articles)} articles to MongoDB.")
        return news_articles

    print("No news articles found.")
    return [{"message": f"No news articles found for {ticker}."}]





# Fetch Stock Data API
@api_view(["GET"])
def get_stock_data(request, ticker):
    """
    Fetch the last 5 days of stock data and save to PostgreSQL.
    """
    ticker = ticker.upper()

    try:
        # Fetch stock data
        stock = yf.Ticker(ticker)
        history = stock.history(period="5d")

        if history.empty:
            return Response({"error": f"No stock data found for {ticker}."}, status=404)

        for index, row in history.iterrows():
            StockData.objects.update_or_create(
                ticker=ticker,
                date=index.date(),
                defaults={
                    "open": row["Open"],
                    "high": row["High"],
                    "low": row["Low"],
                    "close": row["Close"],
                    "volume": row["Volume"],
                    "created_at": now(),
                },
            )

        stock_data = [
            {
                "date": index.strftime("%Y-%m-%d"),
                "open": row["Open"],
                "high": row["High"],
                "low": row["Low"],
                "close": row["Close"],
                "volume": row["Volume"],
            }
            for index, row in history.iterrows()
        ]
        return Response({"data": stock_data, "source": "Yahoo Finance"})
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return Response({"error": "Failed to fetch stock data."}, status=500)


# Fetch News Articles API
@api_view(["GET"])
def get_news_articles(request, ticker):
    """
    Fetch the latest news articles for a given ticker symbol.
    """
    ticker = ticker.upper()

    existing_news = list(news_collection.find({"ticker": ticker}, {"_id": 0}))
    if existing_news:
        return Response(existing_news)

    news_articles = fetch_and_save_news(ticker)
    return Response(news_articles)
