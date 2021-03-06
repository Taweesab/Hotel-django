from django.http import request,JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core import serializers
from django.db import connection
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *
from .forms import *
from .forms import CustomerRegisterForm, RegisterForm,Editroombooking,Editresbooking
from django.contrib.auth.hashers import check_password, make_password
from .decorators import customer_login_required,staff_login_required
from decimal import Context,Decimal
import datetime as dt

def analytics(request):
    return render(request,'analytics.html',{})

def pivot_data(request):
    context=[*Staff.objects.all(),*Customer.objects.all(),*Customer_booking.objects.all(),
            *Promotion_type.objects.all(),*Room.objects.all(),*Service.objects.all(),*Room_detail.objects.all(),
            *Room_booking.objects.all(),*Buffet_round.objects.all(),*Invoice.objects.all(),*Resbooking.objects.all()]
    data = serializers.serialize('json',context)
    return JsonResponse(data, safe=False)

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

@staff_login_required
def invoice_hotel(request):
    return render(request,'invoice_hotel.html')

@staff_login_required
def resultinvoicehotel(request):
    booking_no = request.POST['booking_no']
    customer_id = request.POST['customer_id']
    date = request.POST['date']
    staff_id = "STF00000003"
    # staff_id = Staff.objects.get(customer_id = request.session['staff_id'])
    print(booking_no)
    def bhID():
        n = Room_booking.objects.count()
        if n == 0:
            return "BYT00000001"
        else:
            return "BYT" + str(n+1).zfill(8)
    invoice_no = bhID()
    if customer_id is not None :
        print("restaurant")
        if Customer.objects.filter(customer_id = customer_id).exists():
            customer = Customer.objects.get(customer_id = customer_id)
            fname  = customer.fname 
            lname = customer.lname
            address = customer.address
        else :
            print("error customer")
            messages.error(request,'No this customerid')
            return render(request,'invoice_hotel.html')
    if customer_id is not None and booking_no is not None:
        if Customer_booking.objects.filter(customer_id= customer_id, booking_no=booking_no).exists():
            customer_booking = Customer_booking.objects.get(customer_id= customer_id, booking_no=booking_no)
            print("DATA PRINT", customer_booking.no)
            no = customer_booking.no
            print(no)
        else :
            print("error book")
            messages.error(request,'No this customerid')
            return render(request,'invoice_hotel.html')
    if no is not None :
        if Room_booking.objects.filter(booking_no = no).exists() :
            hotel = Room_booking.objects.get(booking_no = no)
            print("hotel :",hotel)
            # print("bhsurrogate:",hotel.booking_no_id)
            # print("hotel:",hotel)
            # print("hotel1:", hotel.booking_no_id)
            booking_no_id = hotel.bhsurrogate
            # booking_no_id = hotel.bhsurrogate
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
        else :
            print("error Room_booking")
            messages.error(request,'No this booking_no')
            return render(request,'invoice_hotel.html')
    total_charge = total_charge_hotel
    context={"booking_no":booking_no,"customer_id":customer_id,"date_check_in":date_check_in,"date_check_out":date_check_out,
    "number_guest_hotel":number_guest_hotel,"total_charge_hotel":total_charge_hotel,"fname":fname,"lname":lname,
    "address":address,"total_charge":total_charge,"roomtype":roomtype,
    "numberofroom":numberofroom,"service_name":service_name,"invoice_no":invoice_no,"date":date,"staff_id":staff_id,
    "booking_no_id":booking_no_id}
    return render(request,'resultinvoicehotel.html',context)

@staff_login_required
def finishhotel(request):
    print("finishhhhhhhhh")
    print("data:",request.POST)
    invoiceform = InvoiceHotelForm(request.POST)
    if request.method == 'POST':
        print("POST maa")
        invoiceform = InvoiceHotelForm(request.POST)
        if invoiceform.is_valid() :
            print("sucess")
            invoiceform.save()
            return redirect('home')
        else:
            print(invoiceform.errors)
            messages.info(request, invoiceform.errors)
            return render(request,'resultinvoicehotel.html')
    return redirect('home')

@staff_login_required
def invoice_res(request):
    return render(request,'invoice_res.html')

@staff_login_required
def resultinvoiceres(request):
    resb_no = request.POST['resb_no']
    customer_id = request.POST['customer_id']
    date = request.POST['date']
    # staff_id = Staff.objects.get(customer_id = request.session['staff_id'])
    staff_id = "STF00000003"
    print(resb_no)
    def bhID():
        n = Invoice.objects.count()
        if n == 0:
            return "BYT00000001"
        else:
            return "BYT" + str(n+1).zfill(8)
    invoice_no = bhID()
    print("invoice_no:",invoice_no)
    resb_no = request.POST['resb_no']
    customer_id = request.POST['customer_id']
    total_charge_res = 0
    print("date :",request.POST)
    if customer_id is not None :
        print("restaurant")
        if Customer.objects.filter(customer_id = customer_id).exists():
            print("sucess customer")
            customer = Customer.objects.get(customer_id = customer_id)
            fname  = customer.fname 
            lname = customer.lname
            address = customer.address
        else :
            print("error customer")
            messages.error(request,'No this customerid')
            return render(request,'invoice_res.html')
    if customer_id is not None and resb_no is not None:
        if Customer_booking.objects.filter(customer_id= customer_id, resb_no=resb_no).exists():
            customer_booking = Customer_booking.objects.get(customer_id= customer_id, resb_no=resb_no)
            print()
            print("DATA PRINT", customer_booking.no)
            no = customer_booking.no
            print("noo :",no)
        else :
            print("error book")
            messages.error(request,'No this customerid')
            return render(request,'invoice_res.html')
    if no is not None :
        if Resbooking.objects.filter(resb_no_id = no).exists() :
            res =  Resbooking.objects.get(resb_no_id = no)
            print("res:",res)
            print("ressssssss:",res.id)
            resb_no_id = res.id
            # resb_no_id = res.resb_no
            # print("resb_no_id",resb_no_id)
            eatdate = res.eatdate
            number_guest_res= res.number_guest
            buffet_round1 = res.buffet_round
            total_charge_res = res.total_charge
            buffet_round = buffet_round1.buffet_round
        else :
            print("error Hotel_booking")
            messages.error(request,'No this hotel booking')
            return render(request,'invoice_res.html')

    total_charge = total_charge_res
    context={ "resb_no" : resb_no ,"customer_id" : customer_id , 
    "fname" : fname , "lname" : lname , "address" : address ,
    "total_charge" : total_charge, "total_charge_res":total_charge_res,"eatdate":eatdate,
    "number_guest_res":number_guest_res,"buffet_round":buffet_round,"invoice_no":invoice_no,
    "staff_id":staff_id,"no":no,"date":date,"customer_booking":customer_booking,"resb_no_id":resb_no_id,"res":res}
    return render(request,'resultinvoiceres.html',context)

@staff_login_required
def finishres(request):
    print("finishhhhhhhhh")
    print("data:",request.POST)
    invoiceform = InvoiceRestaurantForm(request.POST)
    if request.method == 'POST':
        print("POST maa")
        # invoiceform = InvoiceForm(request.POST)
        # instance = invoiceform.save(commit=False)
        # instance.resb_no = request.Resbooking
        if invoiceform.is_valid() :
            # 
            #
            # instance.save()
            print("sucess")
            invoiceform.save()
            return redirect('home')
        else:
            print(invoiceform.errors)
            messages.info(request, invoiceform.errors)
            return render(request,'resultinvoiceres.html')
    return redirect('home')



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
            messages.info(request,'Those passwords didn???t match. Try again.')
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
            messages.success(request,'Success')
            return redirect('loginstaff')
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
                return redirect('editstaff_hotel')

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
 
# @staff_login_required(job_titles=['M', 'R', 'HS'])
def look_roombook(request, pk):
    customer_booking = Customer_booking.objects.get(booking_no=pk)
    room =  Room_booking.objects.get(booking_no = customer_booking)
    detail = Room_detail.objects.get(detail_no = room.detail_no.detail_no)
    print("test")
    print(room)
    print(detail)
    return render(request,'Roombook_info.html',{"room":room,"no":pk,"detail":detail})

# @staff_login_required(job_titles=['M', 'R', 'RS'])
def look_restbook(request, pk):
    customer_booking = Customer_booking.objects.get(resb_no = pk)
    print(customer_booking)
    table =  Resbooking.objects.get(resb_no = customer_booking)
    print(table.resb_no)
    print(table.eatdate)
    return render(request,'Restbook_info.html',{"table":table,"no":pk})


def showresultroom(request):
    n1 = n2 = n3 = 0
    if request.method == "POST":
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        # print(type(check_in))
        # print(check_out)
        result = Room_booking.objects.filter(date_check_in__gte = check_in,date_check_out__lte = check_out)
        # detail = Room_detail.objects.filter(roomtype = "Junior Suite")
        # result = Room_booking.objects.filter(desc__contains=filter,room_booking__name__contains=detail,date_check_in__lt = check_in,date_check_out__gt = check_out).count()
        # people = Person.objects.raw('SELECT id, first_name, last_name, birth_date FROM myapp_person')
        # result = Room_booking.objects.raw('SELECT COUNT(booking_no_id) FROM hotel_room_booking JOIN hotel_room_detail ON hotel_room_booking.detail_no_id = hotel_room_detail.detail_no WHERE hotel_room_detail.roomtype_id = "Junior Suite" AND hotel_room_booking.date_check_in < "'+check_in+'" AND hotel_room_booking.date_check_out > "'+check_out+'" ')
        print(result)
    else:
        today = dt.date.today()
        tomorrow = today + dt.timedelta(days=1)
        result = Room_booking.objects.filter(date_check_in__gte = today,date_check_in__lte = tomorrow)
        print(result)   
    for i in result:
        print(i.detail_no_id)
        detail = Room_detail.objects.get(detail_no=i.detail_no_id)
        if(detail.roomtype == "Junior Suite"):
            n1 = n1 + 1
        elif(detail.roomtype == "Standard Room"):
            n2 = n2 + 1
        else:
            n3 = n3 + 1
    room1 = Room.objects.get(roomtype = "Junior Suite")
    room2 = Room.objects.get(roomtype = "Standard Room")
    room3 = Room.objects.get(roomtype = "Superior Room")
    n1 = room1.amount - n1
    n2 = room2.amount - n2
    n3 = room3.amount - n3
    if n1 < 0:
        n1 = 0
    if n2 < 0:
        n2 = 0
    if n3 < 0:
        n3 = 0
    
    return render(request,'search_hotel.html',{"room1":room1,"room2":room2,"room3":room3,"n1":n1,"n2":n2,"n3":n3})


def showresultres(request):
    n1 = n2 = 0
    if request.method == "POST":
        searchdate = request.POST.get("searchdate")
        round1 = Resbooking.objects.filter(eatdate=searchdate,buffet_round="lunch")
        round2 = Resbooking.objects.filter(eatdate=searchdate,buffet_round="dinner")
    else:
        today = dt.date.today()
        print(today)
        round1 = Resbooking.objects.filter(eatdate=today,buffet_round="lunch")
        round2 = Resbooking.objects.filter(eatdate=today,buffet_round="dinner")
    
    for i in round1:
        n1 = n1 + i.number_guest
    for j in round2:
        n2 = n2 + j.number_guest
    type1 = Buffet_round.objects.get(buffet_round = "lunch")
    type2 = Buffet_round.objects.get(buffet_round = "dinner")
    n1 = type1.amount - n1
    n2 = type2.amount - n2
    if n1 < 0:
        n1 = 0
    if n2 < 0:
        n2 = 0
    
    return render(request,'search_res.html',{"type1":type1,"type2":type2,"n1":n1,"n2":n2})

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
            print(hotel_book.detail_no)
            print(hotel_book.booking_no)
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
    # return redirect('???home')
    return render(request,'book_hotel4.html')



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

# @staff_login_required(job_titles=['M', 'R', 'HS'])
def logout_staff(request):
    if 'staff_id' in request.session:
        del request.session['staff_id']
    if 'job_title' in request.session:
        del request.session['job_title'] # delete user session
    return redirect('loginstaff')

@customer_login_required
def logout(request):
    if 'customer_id' in request.session:
        del request.session['customer_id'] # delete user session
    return redirect('home')

# @staff_login_required(job_titles=['M', 'R', 'HS'])
def checkroom(request) :
    return render(request,'book_hotel2.html')


# @staff_login_required(job_titles=['M', 'R', 'RS'])
def editstaff_res(request):
    restaurants = Resbooking.objects.all()
    return render(request,'editstaff_res.html',{'restaurants' : restaurants})



# @staff_login_required(job_titles=['M', 'R', 'RS'])
def editres_booking(request,pk):
    resbooking = Resbooking.objects.get(resb_no = pk) 
    if  request.method == "POST":
        num = int(request.POST['number_guest'])
        buffet = request.POST['buffet_round']
        round = Buffet_round.objects.get(buffet_round = buffet)
        total_charge = num * round.charge
        edit_form = Editresbooking(request.POST, instance = resbooking)
        if edit_form.is_valid() :
            edit_form.save()
            print("successs")
            return redirect('editstaff_res')  
        else:
            print(edit_form.errors)
            return redirect("editstaff_res") 
    else:
        print("Error")
    return render(request, 'editres_booking.html',{'resbooking': resbooking})
    # return render(request,'profile.html',{"customer":customer,"customer_booking":customer_booking})



def editroom_booking(request,pk):
    roombooking = Room_booking.objects.get(booking_no = pk)
    detail = Room_detail.objects.get(detail_no = roombooking.detail_no.detail_no) 
    print(pk)
    print("test")
    print(roombooking.detail_no.detail_no)
    if  request.method == "POST":
        # numR = int(request.POST['room_count'])
        # numG = int(request.POST['number_guest'])
        # room = request.POST['roomtype']

        # type = Room_booking.objects.get(roomtype = room)
        # roomservice = request.POST['service_name']
        # service = Room_booking.objects.get(service_name = roomservice)
        # total_charge = (numR * type.price)
        detail_form = RoomdetailForm(request.POST, instance = detail)
        editroom_form = Editroombooking(request.POST, instance = roombooking)
        if editroom_form.is_valid() and detail_form.is_valid():
            detail_room = detail_form.save()
            editroom = editroom_form.save(False)
            editroom.detail_no = detail_room
            editroom.save()
            print("successs")
            return redirect('editstaff_hotel')  
        else:
            print(editroom_form.errors)
            return redirect("editstaff_hotel") 
    else:
        print("Error")
    return render(request, 'editroom_booking.html',{'roombooking': roombooking,'detail':detail})

# @staff_login_required(job_titles=['M', 'R', 'HS'])
def editstaff_hotel(request):
    hotels = Room_booking.objects.all()
    context = {'hotels' : hotels}
    return render(request,'editstaff_hotel.html',context)






    
    
