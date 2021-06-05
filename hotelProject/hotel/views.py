from django.http import request
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import connection 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *
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

@staff_login_required
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

def login(request):
    return render(request,'login.html')

def loginstaff(request):
    return render(request,'loginstaff.html')

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
                return render(request,'register.html')
        else:
            messages.info(request,'Those passwords didn’t match. Try again.')
    return render(request,'register.html')

def register_staff(request):
    form = RegisterForm()
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
    context = {"form": form}
    return render(request,'register_staff.html',context)


def loginstaffaccept(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = Staff.objects.get(email=email)
        # print(user.password)
        # print(check_password(password, user.password))
        if  user is not None :
            if check_password(password, user.password):
                print(user)
                # return 
                request.session['staff_id'] = user.staff_id
                request.session['job_title'] = user.job_title
                return redirect('home')

        messages.error(request,'Not found infomation')
        return redirect('loginstaff')

@customer_login_required
def profile(request):

    customer = Customer.objects.get(customer_id = request.session['customer_id']) 
    if request.method == "POST":
        edit_form = ProfileEditForm(request.POST, instance=customer)
        if edit_form.is_valid :
            edit_form.save()
        return redirect('profile')   
        
    return render(request,'profile.html',{"customer":customer})

@customer_login_required
def bookroom(request):
    Customer_booking.customer_id = request.session['customer_id']
    cst_id = Customer_booking.objects.last()
    context = {"cst_id":cst_id}
    return render(request,'book_hotelcopy.html',context)

def odersummaryhotel(request):
    date_check_in = request.POST["date_check_in"]
    date_check_out = request.POST["date_check_out"]
    number_guest = request.POST["number_guest"]
    roomtype = request.POST["roomtype"]
    service_name = request.POST["service_name"]
    room_count = request.POST["room_count"]
    promotion_code = request.POST["promotion_code"]
    discount= 0
    price_service = 0
    price_room = 0
    total_charge = 0

    if service_name is not None :
        if Service.objects.get(service_name = service_name) :
            service = Service.objects.get(service_name = service_name)
            price_service = service.charge
        else :
            messages.error(request,'No this code')
            return render(request,'book_hotel3copy.html')
    print("service : " ,price_service)

    if roomtype is not None :
        if Room.objects.filter(roomtype=roomtype).exists() :
            room = Room.objects.get(roomtype=roomtype)
            price_room = room.price
        else :
            messages.error(request,'No this code')
            return render(request,'book_hotel3copy.html')
    print("room :" , price_room)
    if promotion_code is not None:
        if Promotion_type.objects.filter(promotion_code=promotion_code).exists() :
            code = Promotion_type.objects.get(promotion_code=promotion_code)
            discount = code.discount
        else :
            messages.error(request,'No this code')
            return render(request,'book_hotel3copy.html')
    print("discount :", discount)
    total_charge = int(price_room)*int(room_count) + int(price_service) - int(discount) 
    context = {"date_check_in": date_check_in, "date_check_out": date_check_out,"number_guest": number_guest,
    "room_count" : room_count,"discount" : discount,"total_charge":total_charge,"service_name":service_name,"roomtype" : roomtype}
    print("context ordersum :",context)
    return render(request,'book_hotel3copy.html',context)

def checkBookingdetail(request):
    if request.method == 'POST':
        date_check_in = request.POST["date_check_in"]
        date_check_out = request.POST["date_check_out"]
        number_guest = request.POST["number_guest"]
        roomtype = request.POST["roomtype"]
        service_name = request.POST["service_name"]
        room_count = request.POST["room_count"]
        discount = request.POST['discount']
        total_charge = request.POST['total_charge']
        print("CHECK DATA", request.POST)
        context = {"date_check_in": date_check_in, "date_check_out": date_check_out,"number_guest": number_guest,
    "room_count" : room_count,"discount" : discount,"total_charge":total_charge,"service_name":service_name,"roomtype" : roomtype}
        context = request.POST
        return render(request,'book_hotel4copy.html',context)

def payhotel(request) :
    if request.method == "POST" :
        room_form = RoomdetailForm(request.POST)
        if room_form.is_valid() :
            room_form.save()

        hotel_form =hotelbookingForm()
        if hotel_form.is_valid() :
            hotel_form.save()
        return render(request,'book_hotel4copy.html')
    else:
        messages.info(request,'Invalid Infomation')
        print("error")
        return render(request,'book_hotel4copy.html')


################## restaurant ####################
@customer_login_required
def bookrest(request):
    customer = Customer.objects.get(customer_id = request.session['customer_id'])
    def brID():
        n = Resbooking.objects.count()
        if n == 0:
            return "BR00000001"
        else:
            return "BR" + str(n+1).zfill(9)
    
    bookno = brID()
    # form = CustomerBookingForm()
    context = {"customer":customer,"bookno":bookno}
    return render(request,'book_res.html',context)

def ordersummaryres(request):
    customer_id = request.POST["customer_id"]
    resb_no = request.POST["resb_no"]
    booking_date = request.POST["booking_date"]
    eatdate = request.POST["eatdate"]
    buffet_round = request.POST["buffet_round"]
    number_guest = request.POST["number_guest"]
    promotion_code = request.POST["promotion_code"]
    bf_round = Buffet_round.objects.get(buffet_round=buffet_round)
    discount = 0

    if promotion_code is not None:
        if Promotion_type.objects.filter(promotion_code=promotion_code).exists() :
            code = Promotion_type.objects.get(promotion_code=promotion_code)
            discount = code.discount
        else :
            messages.error(request,'No this code')
            return render(request,'book_res2.html')
    
    total_charge = (int(number_guest) * bf_round.charge) - discount
    context = {"customer_id":customer_id,"resb_no": resb_no,"booking_date":booking_date,"eatdate": eatdate, "buffet_round": buffet_round,"number_guest": number_guest,"promotion_code": promotion_code,"discount" : discount,"total_charge":total_charge}
    return render(request,'book_res2.html', context)

def paymentres(request):
    
    if request.method == 'POST':
        print("test")
        rest_form = RestBookingForm(request.POST)
        cus_form = CustomerBookingForm(request.POST)
        if rest_form.is_valid() and cus_form.is_valid:
            cus = cus_form.save()
            rest_book = rest_form.save(False)

            rest_book.resb_no = cus
            rest_book.save()

            print("success")
            resb_no = request.POST["resb_no"]
            discount = request.POST["discount"]
            total_charge = request.POST["total_charge"]
            context = {"resb_no":resb_no,"discount":discount,"total_charge":total_charge}
            return render(request,'book_res3.html',context)
            
        else:
            messages.info(request,'Invalid Infomation')
            print("error")
            render(request,'book_res2.html')
    return redirect('home')

# def ComfirmeResbooking(request):
    
#     if request.method == 'POST':
#         print("test")
#         form = RestBookingForm(request.POST)
#         if form.is_valid():
#             form.save()
#             print("success")
#             return redirect('home')
#         else:
#             messages.info(request,'Invalid Infomation')
#             print("error")
#             render(request,'book_res3.html')

def logout_staff(request):
    if 'staff_id' in request.session:
        del request.session['staff_id']
    if 'job_title' in request.session:
        del request.session['job_title'] # delete user session
    return redirect('login')

def logout(request):
    if 'customer_id' in request.session:
        del request.session['customer_id'] # delete user session
    return redirect('home')

def checkroom(request) :
    return render(request,'book_hotel2copy.html')
    
@customer_login_required
def Fform(request):
    print("555555")
    form= FirstForm(request.POST)
    if form.is_valid():
        form.save()
    context= {'form': form }
    
    return render(request, 'book_hotelcopy.html',context)




