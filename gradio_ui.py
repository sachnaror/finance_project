import gradio as gr
import requests
import matplotlib.pyplot as plt
import pandas as pd
from langchain_openai import ChatOpenAI
import os
from langchain.prompts import PromptTemplate

# Configuration
# Please use your own key below
BASE_URL = "http://127.0.0.1:8000/api"
os.environ["OPENAI_API_KEY"] = "sk-proj-Za4KwfA6br8bRV1wSvmDo1yQOQKHeYT-iXWURw2DWUCnfc1ofwVS80FEvE7bYWVrXwnoK_OOnET3BlbkFJk13t4QLYLlcMvFNTf4JSSB-3tns4VrIYQtHkX65EUg5dz6bAbx0cCT_XGoqm3rWRMb-R6hgA"
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)


# Function to fetch stock data and summarize
def fetch_data(ticker):
    ticker = ticker.upper()

    # Fetch stock data
    stock_response = requests.get(f"{BASE_URL}/stock/{ticker}/")
    print("Stock API Response Status:", stock_response.status_code)

    if stock_response.status_code != 200:
        return f"Failed to fetch stock data for {ticker}.", None, None, None

    try:
        stock_data = stock_response.json().get("data", [])
        print("Stock Data:", stock_data)
    except requests.exceptions.JSONDecodeError:
        return f"Invalid response for stock data of {ticker}.", None, None, None

    if not stock_data:
        return f"No stock data found for {ticker}.", None, None, None

    # Generate the stock chart
    try:
        df = pd.DataFrame(stock_data)
        print("Generated DataFrame:\n", df.head())
        plt.figure(figsize=(8, 4))
        plt.plot(df["date"], df["close"], marker="o", label="Close Price", color="blue")
        plt.title(f"Stock Chart for {ticker}")
        plt.xlabel("Date")
        plt.ylabel("Close Price")
        plt.legend()
        plt.grid()
        chart_path = "stock_chart.png"
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()
        print(f"Chart saved at {chart_path}")
    except Exception as e:
        print("Error generating stock chart:", e)
        chart_path = None

    # Generate a stock table
    stock_table = "\n".join([
        f"Date: {row['date']}, Open: {row['open']}, High: {row['high']}, Low: {row['low']}, Close: {row['close']}, Volume: {row['volume']}"
        for row in stock_data
    ])
    print("Generated Stock Table:\n", stock_table)

    # Generate a concise stock summary using OpenAI
    stock_summary_raw = "\n".join([
        f"{row['date']}: Opened at {row['open']}, high of {row['high']}, low of {row['low']}, closed at {row['close']}, volume {row['volume']}"
        for row in stock_data
    ])
    try:
        prompt = PromptTemplate(
            input_variables=["stock_summary"],
            template="Summarize the following stock data into a conversational 4-5 lines:\n{stock_summary}"
        )
        response = llm.invoke(prompt.format(stock_summary=stock_summary_raw))
        concise_summary = response.content.strip()
        print("Generated Stock Summary:\n", concise_summary)
    except Exception as e:
        print("OpenAI API Error:", e)
        concise_summary = "Unable to generate stock summary."

    # Fetch news headlines
    news_response = requests.get(f"{BASE_URL}/news/{ticker}/")
    print("News API Response Status:", news_response.status_code)
    news_headlines = "No news articles found."

    try:
        if news_response.status_code == 200:
            news_articles = news_response.json()
            if isinstance(news_articles, list) and news_articles:
                news_headlines = "\n\n".join([
                    f"**{article.get('title', 'No Title')}**\n[Read More]({article.get('link', 'No Link')})\nDate: {article.get('date', 'No Date')}"
                    for article in news_articles[:5]
                ])
        print("Generated News Headlines:\n", news_headlines)
    except requests.exceptions.JSONDecodeError:
        news_headlines = "Error decoding news data."

    return concise_summary, chart_path, stock_table, news_headlines


# Function to chat with stock and news data
def chat_with_data(ticker, question):
    ticker = ticker.upper()

    # Fetch stock and news data
    stock_response = requests.get(f"{BASE_URL}/stock/{ticker}/")
    news_response = requests.get(f"{BASE_URL}/news/{ticker}/")

    if stock_response.status_code != 200:
        return "Failed to fetch stock data. Please try again."

    stock_data = stock_response.json().get("data", [])
    if not stock_data:
        return "No stock data available for the provided ticker."

    if news_response.status_code != 200:
        return "Failed to fetch news articles. Please try again."

    news_data = news_response.json()
    if not news_data or not isinstance(news_data, list):
        return "No news articles found for the provided ticker."

    # Combine stock and news data
    stock_summary = "\n".join([
        f"{row['date']}: Opened at {row['open']}, high of {row['high']}, low of {row['low']}, closed at {row['close']}, volume {row['volume']}"
        for row in stock_data
    ])
    news_summary = "\n".join([
        f"Title: {article.get('title')}, Link: {article.get('link')}"
        for article in news_data[:5]
    ])
    combined_data = f"Stock Data:\n{stock_summary}\n\nTop News:\n{news_summary}"

    # Generate response using OpenAI
    prompt = PromptTemplate(
        input_variables=["data", "question"],
        template=(
            "You are a stock market expert. Use the following data to answer the user's question:\n"
            "{data}\n\nUser's question:\n{question}\n\nAnswer clearly and concisely."
        ),
    )
    try:
        response = llm.invoke(prompt.format(data=combined_data, question=question))
        return response.content.strip()
    except Exception as e:
        print("OpenAI Error:", e)
        return "An error occurred while processing your question."


# Gradio UI
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("## 📊 Stock Insights Dashboard with Chat")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Input Section")
            ticker_input = gr.Textbox(label="Enter Stock Ticker (e.g., TSLA, AAPL)", placeholder="Enter ticker symbol")
            fetch_btn = gr.Button("Fetch Data", variant="primary")
            clear_btn = gr.Button("Clear")

            gr.Markdown("### 💬 Ask Questions about the Stock or News")
            question_input = gr.Textbox(label="Ask a Question", placeholder="Type your question here...")
            chat_btn = gr.Button("Get Answer")
            chat_output = gr.Textbox(label="Chat Response", interactive=False)

        with gr.Column(scale=2):
            gr.Markdown("### Stock Information and Analysis")
            stock_summary = gr.Textbox(label="Stock Summary", interactive=False)
            stock_chart = gr.Image(label="Stock Chart")
            stock_table = gr.Textbox(label="Stock Data Table", interactive=False)
            news_output = gr.Textbox(label="Top 5 News Headlines", interactive=False)

    # Functionality Binding
    fetch_btn.click(
        fetch_data,
        inputs=ticker_input,
        outputs=[stock_summary, stock_chart, stock_table, news_output]
    )
    chat_btn.click(
        chat_with_data,
        inputs=[ticker_input, question_input],
        outputs=chat_output
    )
    clear_btn.click(
        lambda: ("", None, "", "", ""),
        outputs=[stock_summary, stock_chart, stock_table, news_output, chat_output]
    )

app.launch()
