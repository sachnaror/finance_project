
# 🚀 Stock & News Insights App 📈

Welcome to the **Stock & News Insights App** – a powerful tool built to provide **real-time stock data** and the **latest news headlines** for any company using its ticker symbol. This project, housed in the repository `finance_project`, is tailored for developers, investors, and finance enthusiasts, combining ease of use, reliable data, and modern technologies to keep you informed about the stock market! 📊💼

---

## 🎯 What Does the App Do?

The **Stock & News Insights App** serves three key purposes:

1. **Fetch Stock Data:**
   - Retrieve the last **5 days of stock data** (open, high, low, close, and volume) for any company using its ticker symbol.
   - Data is queried live using **Yahoo Finance** and stored in a **PostgreSQL** database for fast retrieval.

2. **Fetch Latest News:**
   - Fetch the **top 5-10 latest news articles** related to the company's ticker symbol.
   - News data is sourced live using **Yahoo Finance** and stored in a **MongoDB** database to ensure scalability and fast reads.

3. **Interactive Chat for Analysis:**
   - Leverage **OpenAI's GPT-3.5 API** to provide a natural language response for user queries based on stock data and news.
   - Users can ask questions like, *"What is the best day to invest?"* or *"Summarize the stock trends for the past week."* and get intelligent answers.

---

## 📹 Watch the Video Walkthrough Here:

<a href="https://youtu.be/ePyz2ZlIK0M" target="_blank">
    <img src="https://img.youtube.com/vi/ePyz2ZlIK0M/0.jpg" alt="Watch the Video Walkthrough Here" width="600" height="400">
</a>

## 🛠 Tech Stack

The application combines modern web technologies, APIs, and databases to deliver a seamless experience:

### Backend & APIs
- **Django**: The core framework for building the backend API.
- **Django REST Framework (DRF)**: Enables creating RESTful APIs for fetching and serving stock/news data.
- **yfinance**: Fetches stock data from Yahoo Finance.
- **Selenium**: Scrapes live news headlines using a headless browser configured with a proxy.
- **BeautifulSoup**: Parses the scraped Yahoo Finance page to extract clean news content.
- **Requests**: Handles API calls and proxy connections to external data sources.

### Databases
- **PostgreSQL**: Stores historical stock data for persistence and efficient querying.
- **MongoDB**: Saves news articles, ensuring a scalable and document-based solution.

### AI Integration
- **OpenAI API (GPT-3.5-Turbo)**: Provides intelligent, human-like responses to questions about stock trends and news insights.

### UI & User Interaction
- **Gradio**: A powerful UI library that creates a user-friendly, interactive web interface for:
   - Viewing stock summaries, charts, and tables.
   - Fetching news headlines.
   - Asking questions using an AI-powered chatbot.
- **Matplotlib**: Generates stock price charts for visualization.

### Proxy & Browser Automation
- **PacketStream Proxy**: Ensures dynamic IPs for scraping news content without getting blocked.
- **ChromeDriver + Selenium Options**: Runs a headless browser in the background for smooth scraping.

---

## 🧩 How It Works

### 1. **Stock Data Retrieval** 🗂️
- The user inputs a **stock ticker symbol** (e.g., `AAPL`, `TSLA`, `MSFT`).
- A request is sent to the **Django API**, which queries the **Yahoo Finance API** (via `yfinance`).
- The retrieved stock data (5 days of historical data) is stored in a **PostgreSQL** database.
- The backend then returns:
   - A **stock summary** in human-readable format using OpenAI's GPT API.
   - A **stock price chart** plotted using Matplotlib.
   - A tabular format of stock data for detailed insights.

### 2. **News Retrieval** 📰
- The user queries for news related to the company's ticker symbol.
- **Selenium** (with a proxy) navigates to Yahoo Finance News and extracts the latest headlines using **BeautifulSoup**.
- The parsed news is saved in **MongoDB** to ensure future requests are faster.
- The backend returns a list of top 5-10 **news headlines**, including:
   - **Title** of the news.
   - **Link** to the full article.
   - **Date** of publication.

### 3. **Interactive Chat** 💬
- Users can ask questions in natural language, like:
   - *"What are the stock trends for this week?"*
   - *"Summarize the latest news headlines for this company."*
- The app combines **stock data** and **news data** into a single dataset.
- OpenAI's GPT-3.5 API processes the data and provides an insightful, conversational response.

---

## ⚙️ System Workflow

1. **Frontend (Gradio):**
   - Users interact with a simple and intuitive UI.
   - Provides inputs (e.g., ticker symbols, questions) and fetches outputs (stock charts, summaries, and news).

2. **Backend (Django + DRF):**
   - Handles requests from Gradio.
   - Fetches and processes stock and news data.
   - Uses OpenAI API for natural language processing.

3. **Databases:**
   - **PostgreSQL** for structured stock data.
   - **MongoDB** for unstructured news articles.

4. **External Tools:**
   - **yfinance** for stock data.
   - **Selenium + BeautifulSoup** for news scraping.

---

## 🔥 Features

1. **Dynamic Stock Data:**
   - Retrieve accurate and up-to-date stock data with charts and tables.

2. **Real-Time News Headlines:**
   - Fetch the latest company news dynamically using Selenium with proxy support.

3. **AI-Powered Chat:**
   - Get smart, concise insights and summaries using OpenAI's GPT-3.5 API.

4. **Interactive UI:**
   - Use Gradio for seamless interaction with stock data, news, and the AI chatbot.

---

## 🚀 How to Run the App

 Clone the github repo (because, ofcourse :~)

```bash
 git clone https://github.com/sachnaror/finance_project.git
```

### 1. **Install Dependencies**
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### 2. **Set Up Environment Variables**
Create a `.env` file with:
```env
OPENAI_API_KEY=YOUR_OPENAI_KEY
MONGO_URI=mongodb://localhost:27017/
PROXY_URL=http://user:pass@proxy.packetstream.io:31112
CHROME_DRIVER_PATH=/usr/local/bin/chromedriver
```

### 3. **Run the Backend Server**
Start the Django development server:
```bash
python manage.py runserver
```

### 4. **Launch the Gradio App**
Run the Gradio UI:
```bash
python gradio_ui.py
```

Access the app at: [http://127.0.0.1:7860/](http://127.0.0.1:7860/)

---

## 🛡️ Why This App Stands Out
- Combines **real-time stock and news data** for a complete analysis.
- Integrates **AI for smart insights** to assist financial decisions.
- Built on a **scalable, modern tech stack**.
- Ensures smooth scraping with **proxy configuration**.
- User-friendly and highly interactive UI powered by **Gradio**.

---

## 🏆 Conclusion

The **Stock & News Insights App** is a one-stop solution for anyone needing **real-time market insights**, whether for personal analysis or financial decision-making. By seamlessly combining **live stock data**, **news scraping**, and **AI-powered insights**, the app provides actionable information in a user-friendly interface.

Stay informed. Stay ahead. 🚀

---

## 🔗 Future Enhancements
- Adding support for **technical indicators** like moving averages.
- Enabling **real-time alerts** for stock price changes.
- Expanding AI features for **detailed financial analysis**.

---

## 🎨 Preview Image

<img src="resources/image.png" alt="Preview Image" width="600" height="500">




# API Endpoints Documentation

## 1. Fetch Stock Data

### Endpoint
```
GET /api/stock/{ticker}/
```

### Description
This API endpoint fetches the last **5 days of stock data** for a given company ticker symbol from Yahoo Finance and saves the data to the PostgreSQL database.

### Parameters
| Parameter | Type   | Required | Description                                   |
|-----------|--------|----------|-----------------------------------------------|
| `ticker`  | string | Yes      | The stock ticker symbol (e.g., `AAPL`, `TSLA`) |

### Response
- If successful:
```json
{
    "data": [
        {
            "date": "2024-12-11",
            "open": 186.70,
            "high": 196.71,
            "low": 186.26,
            "close": 196.71,
            "volume": 41664500
        },
        {
            "date": "2024-12-10",
            "open": 184.54,
            "high": 188.03,
            "low": 182.67,
            "close": 186.53,
            "volume": 34317400
        }
    ],
    "source": "Yahoo Finance"
}
```

- If no data is found:
```json
{
    "error": "No stock data found for {ticker}."
}
```

### Usage
- **Purpose**: Retrieve recent stock performance (open, high, low, close, and volume).
- **Example**:
```bash
curl http://127.0.0.1:8000/api/stock/AAPL/
```

---

## 2. Fetch News Articles

### Endpoint
```
GET /api/news/{ticker}/
```

### Description
This endpoint fetches the **top 5-10 latest news articles** for the given company ticker symbol from Yahoo Finance using Selenium and saves the results to MongoDB.

### Parameters
| Parameter | Type   | Required | Description                                   |
|-----------|--------|----------|-----------------------------------------------|
| `ticker`  | string | Yes      | The stock ticker symbol (e.g., `AAPL`, `TSLA`) |

### Response
- If successful:
```json
[
    {
        "ticker": "AAPL",
        "title": "Apple Launches New MacBook Pro",
        "link": "https://finance.yahoo.com/news/apple-launches-new-macbook-pro-120000123.html",
        "date": "2024-12-15T10:00:00"
    },
    {
        "ticker": "AAPL",
        "title": "Apple Stock Rises Amid Positive Earnings",
        "link": "https://finance.yahoo.com/news/apple-stock-rises-091200123.html",
        "date": "2024-12-14T14:30:00"
    }
]
```

- If no articles are found:
```json
[
    {"message": "No news articles found for {ticker}."}
]
```

### Usage
- **Purpose**: Retrieve recent financial news and headlines for a given stock ticker.
- **Example**:
```bash
curl http://127.0.0.1:8000/api/news/TSLA/
```

---

## 3. Fetch Stock Data and News in Gradio Dashboard

### Usage within Gradio UI

- **Fetch Stock Data**:
   - Enter the ticker symbol (e.g., `TSLA` or `AAPL`) and click **Fetch Data**.
   - Displays:
     1. A stock summary generated by OpenAI.
     2. A stock chart visualizing the closing prices over 5 days.
     3. A table with stock data (open, high, low, close, and volume).
     4. The top 5 latest news articles for the stock.

- **Ask Questions About Stock and News**:
   - Use the chat section to ask questions related to the stock's recent data or news articles.
   - Example questions:
     - "What is the stock's trend over the past 5 days?"
     - "Should I consider investing in TSLA based on recent news?"

- **Clear Data**:
   - Clears all outputs (chart, table, and news).

---

## Example Gradio API Workflow

1. **Input Stock Ticker**:
   User enters a valid ticker symbol (e.g., `TSLA`) into the input box.

2. **Fetch Stock and News Data**:
   - The `GET /api/stock/{ticker}/` endpoint fetches stock data and displays it.
   - The `GET /api/news/{ticker}/` endpoint fetches news headlines and shows top 5 results.

3. **User Interaction with Chat**:
   - The Gradio app combines both stock and news data.
   - User asks a question, and OpenAI generates an answer.

---

## Debugging Tips for Endpoints

1. **Stock Data**:
   - Ensure the `yfinance` library is using a proxy if requests are being blocked.
   - Debugging logs will print if there’s an issue fetching or saving data.

2. **News Data**:
   - Ensure that the Selenium ChromeDriver setup is correct.
   - Validate proxy usage for accessing Yahoo Finance without IP blocking.
   - Increase wait times using `WebDriverWait` and debug page sources.

3. **General**:
   - Check MongoDB and PostgreSQL configurations for data saving issues.
   - Use curl or Postman to test endpoints independently.

---

## Full Example API Request

1. Fetch Stock Data:
```bash
curl http://127.0.0.1:8000/api/stock/GOOGL/
```

2. Fetch News Articles:
```bash
curl http://127.0.0.1:8000/api/news/GOOGL/
```

3. Expected Response in Gradio UI:
   In the Gradio UI, this response will summarize both stock data and news, generating a user-friendly chart and a concise summary.

---

By integrating these endpoints into the **Gradio-based dashboard**, users can interactively analyze stock data, review news, and get AI-powered insights seamlessly. 🚀
