from django.contrib.auth import get_user_model
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from stocks.models import Stock,PriceHistory
from accounts.models import  Order ,Customer 
from accounts.views import fetch_order_info
from trading_algo.views import place_order, orderbook,update_orderbook 
from trading_algo.models import Transaction
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
import io
import base64
import urllib


def stocksinfo(request, ticker):
    current_user = request.user.customer
    stock_ticker = str(ticker)
    stock_list = Stock.objects.all()
    current_stock = Stock.objects.filter(ticker=stock_ticker).first()
    update_orderbook(orderbook,current_stock)
    transactionss  = Transaction.objects.filter(stock=current_stock).order_by('-timestamp').all()
    graph = plot_stock(current_stock)
    open_orders, completed_orders = fetch_order_info(current_user)

    if request.method == 'POST':
        quantity = request.POST['quantity']
        price = request.POST['price'] 
        side = request.POST['side']
        curr_stock = get_object_or_404(Stock, ticker=stock_ticker)
        place_order(current_user, curr_stock, side, quantity, price)
        return HttpResponseRedirect(request.path_info)
    
    open_orders, completed_orders = fetch_order_info(current_user)
    context = {"current_stock": current_stock, 'stock_list': stock_list, 'orderbook': orderbook ,"open_orders":open_orders, 'completed_orders':completed_orders,'transactionss':transactionss,'graph':graph}
    return render(request, 'stocks/stockinfo.html', context=context)

def plot_stock(current_stock):
    price_history = PriceHistory.objects.filter(stock=current_stock).order_by('date')
    
    dates = [entry.date for entry in price_history]
    prices = [entry.price for entry in price_history]
    
    fig = plt.figure(figsize=(10,6))
    plt.plot(dates, prices)
    plt.xticks(rotation=90)
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    return uri
    