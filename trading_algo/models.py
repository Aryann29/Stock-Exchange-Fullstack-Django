from django.db import models
from accounts.models import Customer
from stocks.models import Stock



class Bid(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    quantity = models.IntegerField()
    total_quantity = models.PositiveIntegerField(default=0) # Track filled quantity

    def __str__(self):
        return f"{self.user.name} {self.stock.name}  {self.total_quantity} {self.price} "
    
    @property
    def order_type(self):
        return "Bid"
    
    def get_remaining_quantity(self):
        return self.total_quantity - self.quantity 
    
    def open_order_total(self):
        return  (self.total_quantity - self.quantity) * self.price 
    
    def completed_order_total(self):
        return  self.total_quantity * self.price 

class Ask(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)  
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    quantity = models.IntegerField()
    total_quantity = models.PositiveIntegerField(default=0)  # Track filled quantity

    def __str__(self):
        return f"{self.user.name} {self.stock.name}  {self.total_quantity} {self.price} "
    
    @property
    def order_type(self):
        return "Ask"
        
    def get_remaining_quantity(self):
        return self.total_quantity - self.quantity 
    
    def open_order_total(self):
        return  (self.total_quantity - self.quantity)* self.price 
    
    def completed_order_total(self):
        return  self.total_quantity * self.price 

class Transaction(models.Model):
    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='buyer')  
    seller = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='seller')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    TRANSACTION_TYPES = [
        ('Bought', 'Bought'),
        ('Sold', 'Sold'),
    ]
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPES, null=True, blank=True)