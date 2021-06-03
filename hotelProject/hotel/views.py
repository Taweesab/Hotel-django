from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.db import connection 



# Create your views here.
def home(request):
    return render(request,'index.html')

def dinning(request):
    return render(request,'rest.html')

def room(request):
    return render(request,'room.html')

def promotion(request):
    allpromotion = promotion_type.objects.all()
    context = {'allpromotion' : allpromotion}
    return render(request,'promotion.html',context)

def contact(request):
    return render(request,'contact.html')

def moreinfo1(request):
    return render(request,'info_room1.html')

def moreinfo2(request):
    return render(request,'info_room2.html')

def moreinfo3(request):
    return render(request,'info_room3.html')

# def booknow(request):
#     return render(request,'book_hotel.html')

def odersummary(request):
    result = room_booking.objects.all()
    context = {'result' : result}
    return render(request,'book_hotel2.html',context)

def payment(request):
    return render(request,'book_hotel3.html')

# def add(request):
#     return render(request,'book_hotel.html')

# def back3(request):
#     return render(request,'book_hotel2.html')

def login(request):
    return render(request,'login.html')

def loginaccept(request):
    username = request.POST['username']
    password = request.POST['password']

    #Check username, password
    user = auth.authenticate(username=username,password=password)
    
    if user is not None :
        auth.login(request,user)
        return redirect('/')
    else :
        messages.info(request,'Not found infomation')
        return redirect('login.html')

def bookroom(request):
    if request.user.is_authenticated:
        if request.method == "POST" :
                saveobj = room_booking()
                saveobj.date_check_in = request.POST.get('checkin')
                saveobj.date_check_out = request.POST.get('checkout')
                saveobj.save()


        return render(request,'book_hotel.html')
    else:
        messages.info(request,'Please Log in')
        return login(request)

def profile(request):
    return render(request,'profile.html')

def bookrest(request):
    if request.user.is_authenticated:
        return render(request,'book_res.html')
    else:
        messages.info(request,'Please Log in')
        return login(request)

# def res1(request):
#     return render(request,'book_res.html')

def res2(request):
    return render(request,'book_res2.html')

def res3(request):
    return render(request,'book_res3.html')


