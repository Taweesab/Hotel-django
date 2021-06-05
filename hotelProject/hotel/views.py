from django.http import request
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import connection 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *
# from .forms import CreateUserForm
from .forms import *
from .forms import CustomerRegisterForm, RegisterForm
from django.contrib.auth.hashers import check_password, make_password
from .decorators import staff_login_required,customer_login_required



# Create your views here.
def home(request):
    return render(request,'index.html')

def dinning(request):
    return render(request,'rest.html')

def room(request):
    return render(request,'room.html')

def promotion(request):
    allpromotion = Promotion_type.objects.all()
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

def odersummaryhotel(request):
    return render(request,'book_hotel3copy.html')

def paymenthotel(request):
    return render(request,'book_hotel4copy.html')

def login(request):
    return render(request,'login.html')

def loginaccept(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = Customer.objects.get(email=email)
        # print(user.password)
        # print(check_password(password, user.password))
        if  user is not None :
            if check_password(password, user.password):
                print(user)
                # return 
                request.session['customer_id'] = user.customer_id
                return redirect('home')

        messages.error(request,'Not found infomation')
        return redirect('login')

def register(request):

    if request.method == 'POST':
        if request.POST['password'] == request.POST['repassword']:
            if Customer.objects.filter(email=request.POST['email']).exists():
                messages.info(request,'This e-mail is used')
                return render(request,'register.html')
            form = CustomerRegisterForm(request.POST)
            if form.is_valid():
                new_user = form.save(commit=False)
                new_user.password = make_password(new_user.password)
                new_user.save()
                messages.success(request,'Success')
                return redirect('login')
            else:
                messages.info(request, form.errors)
                return render(request,'register_staff.html')
        else:
            messages.info(request,'Those passwords didn’t match. Try again.')
    return render(request,'register.html')

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

# @customer_login_required
# def bookroom(request):
#     if request.method == "POST" :
#         saveobj = Room_booking()
#         saveobj.date_check_in = request.POST.get('checkin')
#         saveobj.date_check_out = request.POST.get('checkout')
#         saveobj.save()
#     return render(request,'book_hotel.html')

@customer_login_required
def profile(request):

    customer = Customer.objects.get(customer_id = request.session['customer_id']) 
    if request.method == "POST":
        edit_form = ProfileEdit(request.POST, instance=customer)
        if edit_form.is_valid :
            edit_form.save()
        return redirect('profile')   
        
    return render(request,'profile.html',{"customer":customer})

@customer_login_required
def bookroom(request):
    print("fggggg)")
    if request.method == "POST" :
        print("fggggg")
        form = hotelbookingForm(request.POST)
        print("data :" , request.POST)
        if form.is_valid():
            
        #    bookhotel = form.save(commit=False)
        #    bookhotel.save()
           form.save_m2m()
           print(request.POST)
    return render(request,'book_hotelcopy.html')
    
@customer_login_required
def bookrest(request):
    return render(request,'book_res.html')

def ordersummaryres(request):
    date = request.POST["date"]
    buffet_round = request.POST["buffet_round"]
    number_guest = request.POST["number_guest"]
    promotion_code = request.POST["promotion_code"]
    total_charge = number_guest * Buffet_round.charge(buffet_round=buffet_round) - Promotion_type.discount(promotion_code=promotion_code)
    context = {"date": date, "buffet_round": buffet_round,"number_guest": number_guest,"promotion_code": promotion_code,"total_charge": total_charge}
    return render(request,'book_res2.html', context)

def paymentres(request):
    if request.method == 'POST':
        
        form = RegisterForm(request.POST)
        if form.is_valid():
            
            new_user.save()
        else:
            messages.info(request, form.errors)
            render(request,'register_staff.html')
        
    return render(request,'book_res3.html')



# def reser(request) :
#     if request.method == "POST" :
#                 saveobj = room_booking()
#                 saveobj.date_check_in = request.POST['checkin']
#                 saveobj.date_check_out = request.POST['checkout']
#                 print(request.POST('checkin'))
#                 print(request.POST('checkout'))
#                 saveobj.save()
#                 return render(request,'book_hotel.html')

    # if request.method == "POST":
    #     form  = bookhotel(request.POST)
    #     if  form .is_valid():
    #         form .save()
    #         print(request.POST)

def logout_staff(request):
    if 'staff_id' in request.session:
        del request.session['staff_id'] # delete user session
    return redirect('login')

def logout(request):
    if 'customer_id' in request.session:
        del request.session['customer_id'] # delete user session
    return redirect('home')

def checkroom(request) :
    return render(request,'book_hotel2copy.html')
