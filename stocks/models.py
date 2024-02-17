from django.db import models
from django.utils import timezone


class Stock(models.Model):
    ticker = models.CharField(max_length=15)
    name = models.CharField(max_length=200)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return f"{self.ticker} - {self.name}"
    
class PriceHistory(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)  # Date when the price was recorded
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the stock on the given date

    class Meta:
        ordering = ['-date']  # Ordering by date in descending order by default

    def __str__(self):
        return f"{self.stock} - {self.date}: {self.price}"

    @classmethod
    def add_new_price(cls, stock, price, date=None):
        """
        Add a new price record for a stock.
        If date is not provided, the current date will be used.
        """
        if date is None:
            date = timezone.now().date()
        cls.objects.create(stock=stock, date=date, price=price)
    

class OrderBook(models.Model):
    pass