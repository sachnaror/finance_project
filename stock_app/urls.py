from django.urls import path
from .views import get_stock_data, get_news_articles

urlpatterns = [
    path("stock/<str:ticker>/", get_stock_data, name="stock_data"),
    path("news/<str:ticker>/", get_news_articles, name="news_articles"),
]
