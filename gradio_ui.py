import gradio as gr
import requests

def fetch_stock_data(ticker):
    response = requests.get(f"http://127.0.0.1:8000/api/stock/{ticker}/")
    return response.json()["data"]

def fetch_news_articles(ticker):
    response = requests.get(f"http://127.0.0.1:8000/api/news/{ticker}/")
    return response.json()

iface = gr.Interface(
    fn=lambda ticker: (fetch_stock_data(ticker), fetch_news_articles(ticker)),
    inputs="text",
    outputs=["json", "json"],
    title="Stock Data and News Fetcher",
    description="Enter a stock ticker (e.g., MSFT) to fetch stock prices and related news.",
)

iface.launch()
