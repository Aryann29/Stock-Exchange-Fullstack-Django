from django.contrib import admin
from .models import Ask,Bid,Transaction
# Register your models here.
admin.site.register(Ask)
admin.site.register(Bid)
admin.site.register(Transaction)