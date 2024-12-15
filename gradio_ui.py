import gradio as gr
import requests

def fetch_stock_and_news(ticker):
    ticker = ticker.upper()

    # Fetch stock data
    stock_response = requests.get(f"http://127.0.0.1:8000/api/stock/{ticker}/")
    stock_data = stock_response.json()

    stock_output = "\n".join([
        f"Date: {item['date']}, Open: {item['open']}, High: {item['high']}, "
        f"Low: {item['low']}, Close: {item['close']}, Volume: {item['volume']}"
        for item in stock_data.get("data", [])
    ]) if stock_data.get("data") else stock_data.get("message", "No stock data available.")

    # Fetch news articles
    news_response = requests.get(f"http://127.0.0.1:8000/api/news/{ticker}/")
    news_data = news_response.json()

    news_output = "\n".join([
        f"Title: {item['title']}\nLink: {item['link']}\nDate: {item['date']}"
        for item in news_data
    ]) if isinstance(news_data, list) else news_data.get("message", "No news available.")

    return stock_output, news_output

# Gradio Interface
iface = gr.Interface(
    fn=fetch_stock_and_news,
    inputs="text",
    outputs=["text", "text"],
    title="Stock and News Fetcher",
    description="Enter a stock ticker symbol (e.g., AAPL, TSLA, AMZN) to fetch stock data and the latest news headlines."
)

iface.launch()
