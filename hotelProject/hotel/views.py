from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import connection 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *
from .forms import CreateUserForm, RegisterForm
from django.contrib.auth.hashers import check_password, make_password
from .decorators import staff_login_required



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
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = Staff.objects.get(email=email)
        # print(user.password)
        # print(check_password(password, user.password))
        if check_password(password, user.password):
            print(user)
            # return 
            request.session['staff_id'] = user.staff_id
            return redirect('home')

        return redirect('login')
        #Check username, password
        # if user is not None :
        #     login(request,user)
        #     return redirect('home')
        # else :
        #     messages.info(request,'Not found infomation')
        #     return redirect('login')
    

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Success')
            return redirect('login')
    
    context = {'form':form}
    return render(request,'register.html',context)

def register_staff(request):

    if request.method == 'POST':
        if Staff.objects.filter(email=request.POST['email']).exists():
            return 
        # request.POST['password'] = make_password(request.POST['password'])
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.password = make_password(new_user.password)
            new_user.save()
        else:
            messages.info(request, form.errors)
            render(request,'register_staff.html')
        

    return render(request,'register_staff.html')


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

@staff_login_required
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


def logout(request):
    if 'staff_id' in request.session:
        del request.session['staff_id'] # delete user session
    return redirect('login')