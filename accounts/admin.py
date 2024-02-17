from django.contrib import admin
from .models import Customer,UserStockBalance,Order

admin.site.register(Customer)
admin.site.register(UserStockBalance)
admin.site.register(Order)
