from django.urls import path
from .views import stocksinfo

urlpatterns = [
    path("<str:ticker>", stocksinfo, name='stocksinfo'),
]
