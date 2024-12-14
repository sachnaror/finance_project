import gradio as gr
import requests

def fetch_stock_and_news(ticker):
    ticker = ticker.upper()

    # Fetch stock data
    stock_response = requests.get(f"http://127.0.0.1:8000/api/stock/{ticker}/")
    stock_data = stock_response.json()
    stock_output = stock_data.get("data", [{"Error": stock_data.get("message", "No stock data available.")}])

    # Fetch news articles
    news_response = requests.get(f"http://127.0.0.1:8000/api/news/{ticker}/")
    news_data = news_response.json()
    news_output = news_data if isinstance(news_data, list) else [{"Error": news_data.get("message", "No news available.")}]

    # Format outputs
    formatted_stock = "\n".join([f"Date: {item['date']}, Close: {item['close']}, Volume: {item['volume']}" for item in stock_output[:5]])
    formatted_news = "\n".join([f"Title: {item['title']}\nLink: {item['link']}" for item in news_output])

    return formatted_stock, formatted_news

# Gradio UI
iface = gr.Interface(
    fn=fetch_stock_and_news,
    inputs="text",
    outputs=["text", "text"],
    title="Stock Data and News Fetcher",
    description="Enter a stock ticker symbol (e.g., AAPL, TSLA) to fetch live stock data and top 5 latest news headlines."
)

iface.launch()
