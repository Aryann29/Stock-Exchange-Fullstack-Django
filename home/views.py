from django.shortcuts import render , HttpResponse
from stocks.models import Stock


def home(request):
    stock_list = Stock.objects.all() 
    context = {'stock_list': stock_list}
    
    return render(request,'home.html',context=context)
