"""hotelProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from hotelProject.hotel.forms import bookhotel
from django.contrib import admin
from django.urls import path
from hotel import views
from django.contrib.auth import views as auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('hotel_room/',views.room, name='room'),
    path('dinning_room/',views.dinning, name='rest'),
    path('promotions/',views.promotion, name='promotion'),
    path('contact/',views.contact, name='contact'),
    path('login/',views.login,name='login'),
    path('signup/',views.register,name='register'),
    path('signup_staff/',views.register_staff,name='register_staff'),
    path('loginaccept/',views.loginaccept,name='loginaccept'),
   # path('book_room/',views.bookroom,name='bookroom'),
    path('book_table/',views.bookrest,name='bookrest'),
    path('logout/', views.logout, name='logout'),
    path('moreinfo1/',views.moreinfo1, name='moreinfo1'),
    path('moreinfo2/',views.moreinfo2, name='moreinfo2'),
    path('moreinfo3/',views.moreinfo3, name='moreinfo3'),
    path('odersummaryhotel/',views.odersummaryhotel, name='odersummaryhotel'),
    path('paymenthotel/',views.paymenthotel, name='paymenthotel'),
    path('profile/',views.profile,name='profile'),
    path('ordersummaryres/',views.ordersummaryres,name='ordersummaryres'),
    path('paymentres/',views.paymentres,name='paymentres'),
    path('checkroom/',views.checkroom,name='checkroom')



]
