from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def home(request):
    return render(request,'index.html')

def dinning(request):
    return render(request,'rest.html')

def room(request):
    return render(request,'room copy.html')

def promotion(request):
    return render(request,'promotion.html')

def contact(request):
    return render(request,'contact.html')

<<<<<<< HEAD
def moreinfo1(request):
    return render(request,'info_room1.html')

def moreinfo2(request):
    return render(request,'info_room2.html')

def moreinfo3(request):
    return render(request,'info_room3.html')

def booknow(request):
    return render(request,'book_hotel.html')

def next(request):
    return render(request,'book_hotel2.html')

def next2(request):
    return render(request,'book_hotel3.html')

def add(request):
    return render(request,'book_hotel.html')

def back1(request):
    return render(request,'room.html')

def back2(request):
    return render(request,'book_hotel.html')

def back3(request):
    return render(request,'book_hotel2.html')

def inforoom(request):
    return render(request,'room.html')







=======
def login(request):
    return render(request,'login.html')

def logincheck(request):
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
        return render(request,'book_hotel.html')
    else:
        messages.info(request,'Please Log in')
        return login(request)

def bookrest(request):
    if request.user.is_authenticated:
        return render(request,'book_res.html')
    else:
        messages.info(request,'Please Log in')
        return login(request)
>>>>>>> df842de1bfb4d6248b1b7785907436e34df9a76a
