# 🚀 Stock & News Fetcher App 📈

Welcome to the **Stock & News Fetcher App** (the repo name here is 'finance_project'for this, so don't get confused)– your go-to tool for querying live stock prices and fetching related news articles for your favorite companies. Whether you're a developer, investor, or finance enthusiast, this app simplifies data retrieval and keeps you ahead of the market! 💼✨

---

## 🎯 **Key Features**
- **Stock Data Fetching**: Get live stock data (open, close, high, low prices) from Yahoo Finance.
- **News Articles**: Fetch the latest news articles for a given stock ticker.
- **API Powered**: RESTful APIs built with **Django** to serve stock and news data seamlessly.
- **Dual Database**:
   - 📊 PostgreSQL: Stores structured financial stock data.
   - 📰 MongoDB: Stores unstructured news articles.
- **Simple Interface**: Query with natural inputs using a clean and sleek **Gradio UI**.
- **Quick Insights**: Fetch data with ease and display it as JSON for clarity.

---

## 🛠️ **Tech Stack**
- **Backend**: Django, Django REST Framework
- **Databases**: PostgreSQL (structured data), MongoDB (unstructured data)
- **Data Source**: Yahoo Finance API (via `yfinance` library)
- **Frontend**: Gradio (Simple, responsive UI)
- **Libraries**:
   - `yfinance` for stock data
   - `pymongo` for MongoDB integration
   - `psycopg2` for PostgreSQL integration
   - `pandas` & `matplotlib` for data handling and visualization

---

## 🚀 **Quick Start**

### 1. **Clone the Repository**
```bash
git clone https://github.com/sachnaror/finance_project.git
cd finance_project
```

### 2. **Install Dependencies**
```
pip install django djangorestframework psycopg2 pymongo yfinance pandas matplotlib
```

### 3. **Set Up Databases**
```
	•	PostgreSQL: Create a database named finance_db and configure credentials in settings.py.
	•	MongoDB: Ensure MongoDB is running on localhost:27017.
```
### 4. **Run Migrations**
```
python manage.py makemigrations
python manage.py migrate
```

### 5. **Fetch Data**
```
Run the management command to populate stock and news data:
python manage.py fetch_data
```

### 6. **Start the Server**

Launch the Django development server:
```
python manage.py runserver
```

### 7. **Launch Gradio UI**

Run the Gradio interface for querying data:
```
python gradio_ui.py
```

## 📊 **API Endpoints**

1.	Fetch Stock Data

```
GET /api/stock/{ticker}/
Example: /api/stock/MSFT/
```

2.	Fetch News Articles
```
GET /api/news/{ticker}/
Example: /api/news/MSFT/
```

🎨 User Interface

Input a stock ticker (e.g., MSFT, AAPL) into the Gradio UI to retrieve:

- Stock prices (JSON format).
- Related news articles (title + link).


💡 Why This App?


- 🎯 Simple to Use: Easy querying with a clean interface.
- ⚡ Fast & Reliable: Integrated with Yahoo Finance API for real-time data.
- 🛡️ Modern Tech: Built with Django, PostgreSQL, MongoDB, and Gradio for full-stack efficiency.


🤝 Contributing

Feel free to fork the project, open issues, or submit pull requests. Let’s make this app even better together!
