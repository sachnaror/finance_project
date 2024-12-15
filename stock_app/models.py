from django.db import models

# PostgreSQL Model for Stock Data
class StockData(models.Model):
    ticker = models.CharField(max_length=10)
    date = models.DateField()
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.BigIntegerField()

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # Set once on creation
    updated_at = models.DateTimeField(auto_now=True)      # Updated every time the row is saved

    def __str__(self):
        return f"{self.ticker} - {self.date}"
