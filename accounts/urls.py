from django.urls import path
from .views import login_page,signup,balance_page
 
urlpatterns = [
    path('login/', login_page,name='login_page'),
    path('signup/', signup,name='signup'),
    path('balance/', balance_page, name='balance_page'),
]
