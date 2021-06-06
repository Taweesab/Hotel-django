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
from .decorators import customer_login_required,staff_login_required
from decimal import Decimal
from django.contrib.auth.models import Group

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

def login(request):
    return render(request,'login.html')

def loginstaff(request):
    return render(request,'loginstaff.html')

def invoice_hotel(request):
    return render(request,'invoice_hotel.html')

def resultinvoicehotel(request):
    booking_no = request.POST['booking_no']
    customer_id = request.POST['customer_id']
    print(booking_no)
    if customer_id is not None :
        print("restaurant")
        if Customer.objects.filter(customer_id = customer_id).exists():
            customer = Customer.objects.get(customer_id = customer_id)
            fname  = customer.fname 
            lname = customer.lname
            address = customer.address
        else :
            print("error")
            messages.error(request,'No this customerid')
            return render(request,'invoice_hotel.html')
    if customer_id is not None and booking_no is not None:
        if Customer_booking.objects.filter(customer_id= customer_id, booking_no=booking_no).exists():
            customer_booking = Customer_booking.objects.get(customer_id= customer_id, booking_no=booking_no)
            print("DATA PRINT", customer_booking.no)
            no = customer_booking.no
            print(no)
        else :
            print("error")
            messages.error(request,'No this customerid')
            return render(request,'invoice_hotel.html')
    if no is not None :
        if Room_booking.objects.get(booking_no = no) :
            hotel = Room_booking.objects.get(booking_no = no)
            date_check_in = hotel.date_check_in
            date_check_out = hotel.date_check_out
            number_guest_hotel = hotel.number_guest
            total_charge_hotel = hotel.total_charge
            total_charge =0
            detailno = hotel.detail_no
            roomtype = detailno.roomtype
            numberofroom = detailno.room_count
            service_name = detailno.service_name
            print("roomtype:",roomtype)
            print("date_check_in:",date_check_in)
    total_charge = total_charge_hotel
    context={"booking_no":booking_no,"customer_id":customer_id,"date_check_in":date_check_in,"date_check_out":date_check_out,
    "number_guest_hotel":number_guest_hotel,"total_charge_hotel":total_charge_hotel,"fname":fname,"lname":lname,
    "address":address,"total_charge":total_charge,"roomtype":roomtype,
    "numberofroom":numberofroom,"service_name":service_name}
    return render(request,'resultinvoicehotel.html',context)

def finish(request):
    if request.method == 'POST':
        return redirect('home')

def invoice_res(request):
    return render(request,'invoice_res.html')

def resultinvoiceres(request):
    resb_no = request.POST['resb_no']
    customer_id = request.POST['customer_id']
    total_charge_res = 0
    customer = Customer.objects.get()
    if customer_id is not None :
        print("restaurant")
        if Customer.objects.filter(customer_id = customer_id).exists():
            customer = Customer.objects.get(customer_id = customer_id)
            fname  = customer.fname 
            lname = customer.lname
            address = customer.address
        else :
            print("error")
            messages.error(request,'No this customerid')
            return render(request,'invoice_res.html')
    if customer_id is not None and resb_no is not None:
        if Customer_booking.objects.filter(customer_id= customer_id, resb_no=resb_no).exists():
            customer_booking = Customer_booking.objects.get(customer_id= customer_id, resb_no=resb_no)
            print("DATA PRINT", customer_booking.no)
            no = customer_booking.no
        else :
            print("error")
            messages.error(request,'No this customerid')
            return render(request,'invoice_res.html')
    if no is not None :
        if Resbooking.objects.get(resb_no = no) :
            res =  Resbooking.objects.get(resb_no = no)
            eatdate = res.eatdate
            number_guest_res= res.number_guest
            buffet_round1 = res.buffet_round
            total_charge_res = res.total_charge
            buffet_round = buffet_round1.buffet_round
        else :
            messages.error(request,'No this hotel booking')
            return render(request,'resultinvoiceres.html')

    total_charge = total_charge_res
    context={ "resb_no" : resb_no ,"customer_id" : customer_id , 
    "fname" : fname , "lname" : lname , "address" : address ,
    "total_charge" : total_charge, "total_charge_res":total_charge_res,"eatdate":eatdate,
    "number_guest_res":number_guest_res,"buffet_round":buffet_round}
    return render(request,'resultinvoiceres.html',context)

def loginaccept(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = Customer.objects.get(email=email)
        # print(user.password)
        # print(check_password(password, user.password))
        if user is not None :
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
            # group = Group.objects.get(name='staff')
            # user.groups.add(group)

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
    customer_booking = Customer_booking.objects.filter(customer_id = request.session['customer_id']).order_by('booking_date')
    if request.method == "POST":
        edit_form = ProfileEditForm(request.POST, instance=customer)
        if edit_form.is_valid :
            edit_form.save()
        return redirect('profile')   
        
    return render(request,'profile.html',{"customer":customer,"customer_booking":customer_booking})

@customer_login_required
def bookroom(request):
    customer = Customer.objects.get(customer_id = request.session['customer_id'])
    def bhID():
        n = Room_booking.objects.count()
        if n == 0:
            return "BH000000001"
        else:
            return "BH" + str(n+1).zfill(9)
    
    bookno = bhID()
    # form = CustomerBookingForm()
    context = {"customer":customer,"bookno":bookno}
    return render(request,'book_hotel.html',context)

def odersummaryhotel(request):
    customer_id = request.POST["customer_id"]
    booking_no = request.POST["booking_no"]
    booking_date = request.POST["booking_date"]
    date_check_in = request.POST["date_check_in"]
    date_check_out = request.POST["date_check_out"]
    number_guest = request.POST["number_guest"]
    roomtype = request.POST["roomtype"]
    service = request.POST["service_name"]
    room_count = request.POST["room_count"]
    promotion_code = request.POST["promotion_code"]
    type = Room.objects.get(roomtype=roomtype)
    discount= 0
    price_service = 0
    total_charge = 0
    service_name = ""
    
    if service is not None:
        print(service)
        service = str(service)
        l = len(service)
        new = service[0:l-1]
        s_code = new.split(",")
        for i in s_code:
            if Service.objects.filter(service_code=i).exists() :
                ser = Service.objects.get(service_code=i)
                service_name = service_name + ser.service_name + " " 
                if ser.service_name == "S0003":
                    price_service = price_service + (int(number_guest)*ser.charge)
                else:
                    price_service = price_service + ser.charge
    print(service_name)
    if promotion_code != "":
        if Promotion_type.objects.filter(promotion_code=promotion_code).exists() :
            code = Promotion_type.objects.get(promotion_code=promotion_code)
            discount = code.discount
        else :
            messages.error(request,'No this code')
            return render(request,'book_hotel3.html')    
    else:
        promotion_code = "No"    
    total_charge = int(type.price)*int(room_count) + price_service - discount

    context = {"customer_id":customer_id,"booking_no": booking_no,"booking_date":booking_date,"date_check_in": date_check_in, "date_check_out": date_check_out,
    "number_guest": number_guest,"roomtype":roomtype,"service_name":service_name ,"promotion_code": promotion_code,"room_count":room_count ,"discount" : discount,"total_charge":total_charge}
    return render(request,'book_hotel3.html', context)


def paymenthotel(request) :
    if request.method == 'POST':
    #     date_check_in = request.POST["date_check_in"]
    #     date_check_out = request.POST["date_check_out"]
    #     number_guest = request.POST["number_guest"]
    #     roomtype = request.POST["roomtype"]
    #     service_name = request.POST["service_name"]
    #     room_count = request.POST["room_count"]
    #     discount = request.POST['discount']
    #     total_charge = request.POST['total_charge']
    #     context = {"date_check_in": date_check_in, "date_check_out": date_check_out,"number_guest": number_guest,
    # "room_count" : room_count,"discount" : discount,"total_charge":total_charge,"service_name":service_name,"roomtype" : roomtype}
    #     context = request.POST
        print("CHECK DATA", request.POST)
        cus_form = CustomerHotelForm(request.POST)
        detial_form = RoomdetailForm(request.POST)
        hotel_form = HotelbookingForm(request.POST)
        if hotel_form.is_valid() and cus_form.is_valid() and detial_form.is_valid():
            cus = cus_form.save()
            detial = detial_form.save()
            print(detial.detail_no)
            hotel_book = hotel_form.save(False)

            hotel_book.booking_no = cus
            hotel_book.detail_no = detial
            hotel_book.save()

            print("success")
            booking_no = request.POST["booking_no"]
            discount = request.POST["discount"]
            total_charge = request.POST["total_charge"]
            context = {"booking_no":booking_no,"discount":discount,"total_charge":total_charge}
            return render(request,'book_hotel4.html',context)

        else:
            messages.info(request,'Invalid Infomation')
            print("error")
            return render(request,'book_hotel4.html')
    # return redirect('้home')
    return render(request,'book_hotel4.html',context)


################## restaurant ####################
@customer_login_required
def bookrest(request):
    customer = Customer.objects.get(customer_id = request.session['customer_id'])
    def brID():
        n = Resbooking.objects.count()
        if n == 0:
            return "BR000000001"
        else:
            return "BR" + str(n+1).zfill(9)
    
    bookno = brID()
    # form = CustomerBookingForm()
    context = {"customer":customer,"bookno":bookno}
    return render(request,'book_res.html',context)

def ordersummaryres(request):
    print(request.POST["promotion_code"] is None)
    customer_id = request.POST["customer_id"]
    resb_no = request.POST["resb_no"]
    booking_date = request.POST["booking_date"]
    eatdate = request.POST["eatdate"]
    buffet_round = request.POST["buffet_round"]
    number_guest = request.POST["number_guest"]
    promotion_code = request.POST["promotion_code"]
    bf_round = Buffet_round.objects.get(buffet_round=buffet_round)
    discount = 0

    if promotion_code != "":
        if Promotion_type.objects.filter(promotion_code=promotion_code).exists() :
            code = Promotion_type.objects.get(promotion_code=promotion_code)
            discount = code.discount
        else :
            messages.error(request,'No this code')
            return render(request,'book_res.html')
    else:
        promotion_code = "No"
    print(promotion_code)
    total_charge = (int(number_guest) * bf_round.charge) - discount
    context = {"customer_id":customer_id,"resb_no": resb_no,"booking_date":booking_date,"eatdate": eatdate, "buffet_round": buffet_round,"number_guest": number_guest,"promotion_code": promotion_code,"discount" : discount,"total_charge":total_charge}
    return render(request,'book_res2.html', context)

def paymentres(request):
    
    if request.method == 'POST':
        print("test")
        rest_form = RestBookingForm(request.POST)
        cus_form = CustomerBookingForm(request.POST)
        print(rest_form.is_valid())
        print(cus_form.is_valid())
        if rest_form.is_valid() and cus_form.is_valid():
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
            return render(request,'book_res2.html')
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
    return render(request,'book_hotel2.html')

def editstaff_res(request):
    restaurants = Resbooking.objects.all()
    return render(request,'editstaff_res.html',{'restaurants' : restaurants})

def editstaff_hotel(request):
    hotels = Room_booking.objects.all()
    return render(request,'editstaff_hotel.html',{'hotels' : hotels})
