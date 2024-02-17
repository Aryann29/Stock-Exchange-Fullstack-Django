from django.shortcuts import render, HttpResponse,HttpResponseRedirect,redirect
from trading_algo.models import Ask, Bid
from django.db.models import Q
from itertools import chain
from .models import Customer, UserStockBalance
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout

def login_page(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)


        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')
        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/login.html')


def signup(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        print(email)

        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()
        customer_obj = Customer.objects.create(user=user_obj, name=first_name, )
        return HttpResponseRedirect(request.path_info)
    return render(request,'accounts/register.html')


def logout_page(request):
    return redirect('getting_start')


def balance_page(request):
    current_user = request.user
    customer = Customer.objects.get(user=current_user)
    user_stock_balances = UserStockBalance.objects.filter(user=customer)
    
    # Calculate total value for each stock balance
    for balance in user_stock_balances:
        balance.total_value = balance.quantity * balance.stock.current_price
    
    context = {
        'customer': customer,
        'user_stock_balances': user_stock_balances
    }
    return render(request, 'accounts/balance_page.html', context)

def fetch_order_info(user):
    filled_asks = Ask.objects.filter(user=user, quantity=0)
    filled_bids = Bid.objects.filter(user=user, quantity=0)
    bid_open_orders =  Bid.objects.filter(user=user, quantity__gt=0)
    ask_open_orders = Ask.objects.filter(user=user, quantity__gt=0)
    
    
    completed_orders = list(chain(filled_asks, filled_bids))
    open_orders = list(chain(bid_open_orders, ask_open_orders))
    for order in open_orders:
        print(order.order_type,order.stock.ticker,order.quantity , order.price, order.total_quantity )
    return open_orders,completed_orders
        
        
