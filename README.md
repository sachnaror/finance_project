
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

