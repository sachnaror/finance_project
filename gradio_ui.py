import gradio as gr
import requests
import matplotlib.pyplot as plt
import pandas as pd

BASE_URL = "http://127.0.0.1:8000/api"

def fetch_data(ticker):
    ticker = ticker.upper()

    # Fetch stock data
    try:
        stock_response = requests.get(f"{BASE_URL}/stock/{ticker}/")
        stock_data = stock_response.json().get("data", [])
    except:
        return "Error fetching stock data.", None, None, "Error fetching news."

    if not stock_data:
        return f"No stock data available for {ticker}.", None, None, "No news articles."

    # Fetch news data
    try:
        news_response = requests.get(f"{BASE_URL}/news/{ticker}/")
        news_data = news_response.json().get("news", [])
    except:
        news_data = []

    # Generate Chart
    df = pd.DataFrame(stock_data)
    plt.figure(figsize=(10, 5))
    plt.plot(df["date"], df["close"], marker="o", label="Close Price")
    plt.title(f"Stock Chart for {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    chart_path = "stock_chart.png"
    plt.savefig(chart_path)
    plt.close()

    # Stock Table
    stock_table = "\n".join([
        f"Date: {row['date']}, Open: {row['open']}, High: {row['high']}, Low: {row['low']}, Close: {row['close']}, Volume: {row['volume']}"
        for row in stock_data
    ])

    # News Display
    news_display = "\n".join([
        f"Title: {news['title']}\nLink: {news['link']}\nDate: {news['date']}"
        for news in news_data
    ]) if news_data else "No news articles found."

    return f"Stock data for {ticker} retrieved successfully.", chart_path, stock_table, news_display

# Gradio UI
with gr.Blocks() as app:
    gr.Markdown("## Stock and News Viewer")

    with gr.Row():
        ticker_input = gr.Textbox(label="Enter Stock Ticker")
        fetch_btn = gr.Button("Fetch Data")

    summary_output = gr.Textbox(label="Stock Summary")
    chart_output = gr.Image(label="Stock Chart")
    table_output = gr.Textbox(label="Stock Table")
    news_output = gr.Textbox(label="Top 5 News Headlines")

    fetch_btn.click(fetch_data, inputs=ticker_input, outputs=[summary_output, chart_output, table_output, news_output])

app.launch()
