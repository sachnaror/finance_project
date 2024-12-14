from django.db import models

class StockData(models.Model):
    ticker = models.CharField(max_length=10)
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.BigIntegerField()

    def __str__(self):
        return f"{self.ticker} - {self.date}"

class NewsSource(models.Model):
    ticker = models.CharField(max_length=10)
    link = models.URLField()
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"News for {self.ticker} - {self.link}"
