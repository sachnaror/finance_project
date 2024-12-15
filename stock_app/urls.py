
from django.urls import path
from .views import get_stock_data, get_news_articles

urlpatterns = [
    path('api/stock/<str:ticker>/', get_stock_data, name='get_stock_data'),
    path('api/news/<str:ticker>/', get_news_articles, name='get_news_articles'),
]
