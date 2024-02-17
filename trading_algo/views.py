from django.shortcuts import render,redirect 
from accounts.models import Order
from django.contrib.auth.models import User  # Assuming you're using Django's built-in User model
from .models import Bid,Ask,Transaction 
from accounts.models import Customer ,UserStockBalance
from stocks.models import PriceHistory


from decimal import Decimal
orderbook = {
    
    
}

bids = {}
asks = {}



def place_order(current_user, current_stock, side, quantity, price):
    
    update_orderbook(orderbook, current_stock)
    remaining_qty = execute_order(current_user, current_stock, side, quantity, price)  # Call remaining_quantity function
    # if remaining_qty == 0:
    #     update_orderbook(orderbook, current_stock)
   
    # else:
    if side == 'bid':
        bid_obj = Bid(user=current_user, stock=current_stock, price=price, quantity=remaining_qty, total_quantity=quantity)
        bid_obj.save()
        update_orderbook(orderbook, current_stock)
    else:
        ask_obj = Ask(user=current_user, stock=current_stock, price=price, quantity=remaining_qty,total_quantity=quantity)
        ask_obj.save()
        update_orderbook(orderbook, current_stock)
 

def execute_order(current_user, current_stock, side, quantity, price): 
    remaining_qty = int(quantity)
    price = int(price)
    print(type(current_user))
    if side == 'bid':
        asks = Ask.objects.filter(
            stock=current_stock
        ).order_by('price')

        for ask in asks[::-1]:  
            if ask.price > price:
                continue
                
            if ask.quantity > remaining_qty:
                ask.quantity -= remaining_qty
                ask.save()  
                swap_balances(ask.user, current_user, remaining_qty, price,current_stock)
                return 0
                
            else:
                remaining_qty -= ask.quantity
                swap_balances(ask.user, current_user, remaining_qty, price,current_stock)
                ask.quantity = 0 
                ask.save()
                
    else:
        bids = Bid.objects.filter(
            stock=current_stock
        ).order_by('-price')
        
        for bid in bids:
            if bid.price < price:  
                continue
                
            if bid.quantity > remaining_qty:
                bid.quantity -= remaining_qty
                bid.save()
                swap_balances(current_user, bid.user, remaining_qty, price,current_stock)
                return 0
                
            else:
                remaining_qty -= bid.quantity
                swap_balances(current_user, bid.user, remaining_qty, price,current_stock)
                bid.quantity = 0
                
                bid.save()
                
    return remaining_qty


def swap_balances(user1, user2, qty, price, current_stock):
    
    
    if user1 == user2:
        print("Cannot trade with the same user.")
        return
    user1_stock_balance = user1.userstockbalance_set.get(stock=current_stock)
    
    if user1_stock_balance.quantity < qty :
        print(f"Insufficient stock balance for {user1.name}")
        return
    if user2.balance < qty*price :
        print(f"Insufficient balance for {user2.name}")
        return
    try:
        user1_stock_balance = user1.userstockbalance_set.get(stock__name=current_stock.name)
        user2_stock_balance = user2.userstockbalance_set.get(stock__name=current_stock.name)
    except UserStockBalance.DoesNotExist:
        print("User does not have the specified stock")
        return
    
    user1_stock_balance.quantity -= qty
    user1.balance -= qty * price
    user2_stock_balance.quantity += qty
    user2.balance += qty * price
    
    user1_stock_balance.save()
    user1.save()
    user2_stock_balance.save()
    user2.save()
    
    transaction_type = "Bought" if price > current_stock.current_price else "Sold"
    transaction = Transaction(buyer=user2,seller=user1,stock=current_stock,price=price,quantity=qty,transaction_type=transaction_type)
    transaction.save()
    

    if current_stock.current_price != price:
        current_stock.current_price = price
        current_stock.save() 
         
        PriceHistory.add_new_price(stock=current_stock, price=price)
  
    print(f"Swapped {qty} stocks of {current_stock.name} between User {user1.id} and User {user2.id}.")
    print(f"User {user1.id} new balance: {user1.balance}")
    print(f"User {user2.id} new balance: {user2.balance}")
   




                

def update_orderbook(orderbook,current_stock):

    orderbook.clear()

 
    all_bids = Bid.objects.filter(stock=current_stock).all().order_by('-price').values('price', 'quantity')
    all_asks = Ask.objects.filter(stock=current_stock).all().order_by('price').values('price', 'quantity')


    for bid in all_bids:
        price = bid['price']
        quantity = bid['quantity']
        if price in orderbook:
            orderbook[price]['bids'] += quantity
            all_bids = Bid.objects.all().order_by('-price').values('price', 'quantity')
           
        else:
            orderbook[price] = {'bids': quantity, 'asks': 0}
            all_bids = Bid.objects.all().order_by('-price').values('price', 'quantity')
           
    for ask in all_asks:
        price = ask['price']
        quantity = ask['quantity']
        if price in orderbook:
            orderbook[price]['asks'] += quantity
            
            all_asks = Ask.objects.all().order_by('price').values('price', 'quantity')
        else:
            orderbook[price] = {'bids': 0, 'asks': quantity}
           
            all_asks = Ask.objects.all().order_by('price').values('price', 'quantity')



