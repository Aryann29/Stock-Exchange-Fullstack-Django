from django.db import models
from django.contrib.auth.models import User
from stocks.models import Stock



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    name = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name
    
class UserStockBalance(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    def __str__(self):
        return f"{self.user.name} {self.stock.name}"

class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=3, choices=[('BID', 'bid'), ('ASK', 'ask')])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.name} {self.order_type} {self.stock.name}"
    
    
