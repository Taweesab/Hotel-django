from os import name
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime,date

# Create your models here.
class Staff(models.Model):
    def genID():
        n = Staff.objects.count()
        if n == 0:
            return "STF00000001"
        else:
            return "STF" + str(n+1).zfill(6)

    # user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)       
    staff_id = models.CharField(max_length=12, default=genID, primary_key=True)
    fname = models.CharField(max_length=64, null=False)
    lname = models.CharField(max_length=64, null=False)
    dob = models.DateField(null=False)
    Job_title = (
        ("S", "Staff"),
        ("A", "Admin"),
        ("M", "Manager"),
        ("R", "Receptionist"),
        ("HS", "Hotel Staff"),
        ("RS", "Restaurant Staff"),
    )

    job_title = models.CharField(max_length=5, choices=Job_title, default="S")
    salary = models.FloatField(null=True)
    email = models.EmailField(null=False, unique=True)
    password = models.CharField(max_length=100, null=False)

    def __str__(self) :
        return self.staff_id

class Customer(models.Model):
    def genID():
        n = Customer.objects.count()
        if n == 0:
            return "CST00000001"
        else:
            return "CST" + str(n+1).zfill(8)

    # user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)   
    customer_id = models.CharField(max_length=11, default=genID, null=False, primary_key=True)
    fname = models.CharField(max_length=64, null=False)
    lname = models.CharField(max_length=64, null=False)
    email = models.EmailField(null=False, unique=True)
    password = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=200, null=False)
    tel = models.CharField(max_length=10, null=False, unique=True)

    def fullname(self):
        return self.fname + " " + self.lname

    def __str__(self):
        return self.customer_id

class Customer_booking(models.Model):  
    # def bhID():
    #     n = Room_booking.objects.count()
    #     if n == 0:
    #         return "BH00000001"
    #     else:
    #         return "BH" + str(n+1).zfill(9)

    # customer_surrogate = models.AutoField(primary_key=True) 
    no = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.RESTRICT, null=False)
    booking_no = models.CharField(max_length = 11, null = True,unique = True)
    resb_no = models.CharField(max_length = 11,null = True,unique = True)
    booking_date = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return str(self.no)

class Promotion_type(models.Model):
    promotion_code = models.CharField(max_length=7, null=False, primary_key=True)
    promotion_name = models.CharField(max_length=32, null=False)
    promotion_detail = models.CharField(max_length=500, null = False)
    ptype = (
        ("Hotel", "Hotel"),
        ("Restaurant", "Restaurant"),
    )
    promotion_type = models.CharField(max_length=20,choices=ptype ,null=False,default="Hotel")
    start_date = models.DateField(null=False)
    expire_date = models.DateField(null= False)
    discount = models.FloatField(null=False)

    def __str__(self) :
        return self.promotion_name

class Room(models.Model):
    roomtype = models.CharField(max_length=20, null=False, primary_key=True)
    capacity = models.IntegerField(null = False)
    price = models.FloatField(null=False)
    amount = models.IntegerField(null=False,default=100)

    #try query data   
    def __str__(self) :
        return self.roomtype

class Service(models.Model):
    service_code = models.CharField(max_length=5, null=False, primary_key=True)
    service_name = models.CharField(max_length=20, null = False)
    charge = models.FloatField(null = True)

    #try query data    
    def __str__(self) :
        return self.service_name
    

class Room_detail(models.Model):
    detail_no = models.AutoField(primary_key=True)
    roomtype = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)
    service_name = models.CharField(max_length = 32, null=True)
    room_count = models.IntegerField(null=False)
    def __str__(self) :
        return str(self.detail_no)
    
    
class Room_booking(models.Model):
    bhsurrogate = models.AutoField(primary_key = True)
    booking_no = models.ForeignKey(Customer_booking,on_delete=models.RESTRICT, null=True)
    date_check_in = models.DateField(null = False)
    date_check_out = models.DateField(null = False)
    detail_no = models.ForeignKey(Room_detail, on_delete = models.CASCADE, null = False)
    promotion_code = models.CharField(max_length=7, null=True)
    number_guest = models.IntegerField(null = False)
    total_charge = models.FloatField(null = False)
    payment_method = models.CharField(max_length = 32, null = True)

    #try query data
    # def __str__(self) :
    #     return self.booking_no


class Buffet_round(models.Model):
    # round = (('lunch',"LUNCH"),('dinner',"DINNER"))
    # buffet_round=models.CharField(max_length=64,choices=round,default=False ,null=False)
    buffet_round=models.CharField(max_length=64, primary_key = True ,null=False)
    charge=models.FloatField(null =True)
    amount = models.IntegerField(null=False)

    def __str__(self):
        return self.buffet_round

class Resbooking(models.Model):
    resb_no = models.ForeignKey(Customer_booking, on_delete=models.RESTRICT, null=True)
    promotion_code = models.CharField(max_length=7, null=True)
    number_guest = models.IntegerField(null=False)
    eatdate = models.DateField(null=False)
    buffet_round = models.ForeignKey(Buffet_round, on_delete=models.SET_NULL, null=True)
    total_charge = models.FloatField(null=False)
    paymentmethod = models.CharField(max_length=32, null=False)


class Invoice(models.Model):
    invoice_no = models.CharField(max_length=12, null=False, primary_key=True, unique=True)
    booking_no = models.ForeignKey(Room_booking, on_delete=models.RESTRICT, null=True)
    resb_no = models.ForeignKey(Resbooking, on_delete = models.RESTRICT, null=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.RESTRICT, null=False)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE, null=False)
    tax = models.FloatField(null=False)
    date = models.DateField(null=False)




