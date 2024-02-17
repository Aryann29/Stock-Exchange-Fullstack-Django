from django.shortcuts import render , HttpResponse
from accounts.models import User,Customer
def dashboard(request):
    users = Customer.objects.all()
    
    context = {'users': users}
    return render(request,'dashboard/dashboard.html',context=context)