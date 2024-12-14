from rest_framework.decorators import api_view
from rest_framework.response import Response
from stock_app.models import StockData
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
news_db = client["finance_data"]

@api_view(["GET"])
def get_stock_data(request, ticker):
    stock = StockData.objects.filter(ticker=ticker).values()
    return Response({"data": list(stock)})

@api_view(["GET"])
def get_news_articles(request, ticker):
    news = news_db.news_articles.find({"ticker": ticker})
    return Response([{"title": item["title"], "link": item["link"]} for item in news])
