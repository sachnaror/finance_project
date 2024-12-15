import gradio as gr
import matplotlib.pyplot as plt
from pymongo import MongoClient
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import pandas as pd
import json

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017/")
db = client["finance_data"]
news_collection = db["news_articles"]
stock_collection = db["stock_data"]

# LangChain Configuration (replace with your OpenAI key)
import os
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
llm = OpenAI(temperature=0.5)

# Function to fetch and summarize stock data
def fetch_stock_data(ticker):
    # Retrieve stock data from MongoDB
    stock_data = list(stock_collection.find({"ticker": ticker.upper()}))

    if not stock_data:
        return "No stock data found for this ticker.", "", None

    # Convert to DataFrame
    df = pd.DataFrame(stock_data)

    # Generate Chart
    plt.figure(figsize=(10, 5))
    plt.plot(df["date"], df["close"], label="Close Price", marker="o")
    plt.title(f"Stock Data for {ticker.upper()}")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("stock_chart.png")
    plt.close()

    # Generate Summary using LangChain
    stock_json = json.dumps(stock_data, default=str)
    prompt = PromptTemplate(
        input_variables=["stock_data"],
        template="Summarize the following stock data in 2-4 lines:\n{stock_data}"
    )
    summary = llm(prompt.format(stock_data=stock_json))

    return f"Summary for {ticker.upper()}:\n{summary}", "stock_chart.png", df

# LangChain-powered chat for user questions
def chat_with_data(ticker, question):
    # Retrieve stock and news data from MongoDB
    stock_data = list(stock_collection.find({"ticker": ticker.upper()}))
    news_data = list(news_collection.find({"ticker": ticker.upper()}))

    if not stock_data and not news_data:
        return "No data found for this ticker."

    # Combine data into a JSON string
    combined_data = {
        "stock_data": stock_data,
        "news_data": news_data
    }
    data_json = json.dumps(combined_data, default=str)

    # LangChain prompt
    prompt = PromptTemplate(
        input_variables=["question", "data"],
        template="Answer the following question based on the provided data:\nQuestion: {question}\nData: {data}"
    )
    response = llm(prompt.format(question=question, data=data_json))

    return response

# Gradio UI
def gradio_interface(ticker):
    summary, chart, df = fetch_stock_data(ticker)
    if not df:
        return summary, None, None

    # Format stock data table
    stock_table = "\n".join([
        f"Date: {row['date']}, Open: {row['open']}, High: {row['high']}, Low: {row['low']}, "
        f"Close: {row['close']}, Volume: {row['volume']}"
        for _, row in df.iterrows()
    ])

    return summary, chart, stock_table

# Gradio Chat Interface
def gradio_chatbox(ticker, question):
    return chat_with_data(ticker, question)

# Gradio Layout
with gr.Blocks() as app:
    gr.Markdown("## Stock Data and News Interaction")

    with gr.Row():
        with gr.Column():
            ticker_input = gr.Textbox(label="Enter Stock Ticker (e.g., TSLA, AAPL)")
            submit_btn = gr.Button("Submit")
            clear_btn = gr.Button("Clear")

            # Chatbox for user queries
            gr.Markdown("### Ask a Question about the Stock Data")
            question_input = gr.Textbox(label="Enter your question")
            chat_btn = gr.Button("Ask")
            chat_output = gr.Textbox(label="Chat Response")

        with gr.Column():
            summary_output = gr.Textbox(label="Stock Summary")
            chart_output = gr.Image(label="Stock Chart")
            table_output = gr.Textbox(label="Stock Data Table")

    submit_btn.click(gradio_interface, inputs=ticker_input, outputs=[summary_output, chart_output, table_output])
    chat_btn.click(gradio_chatbox, inputs=[ticker_input, question_input], outputs=chat_output)
    clear_btn.click(lambda: ("", None, ""), outputs=[summary_output, chart_output, table_output])

app.launch()
