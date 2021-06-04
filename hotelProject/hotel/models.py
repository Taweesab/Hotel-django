from os import name
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

    staff_id = models.CharField(max_length=9, default=genID, primary_key=True)
    fname = models.CharField(max_length=64, null=False)
    lname = models.CharField(max_length=64, null=False)
    dob = models.DateField(null=False)
    job_title = models.CharField(max_length=64, null=False)
    salary = models.FloatField(null=False)
    email = models.EmailField(null=False,unique=True)
    password = models.CharField(max_length=100, null=False)

class Customer(models.Model):
    def genID():
        n = Customer.objects.count()
        if n == 0:
            return "CST00000001"
        else:
            return "CST" + str(n+1).zfill(8)
    
    customer_id = models.CharField(max_length=11,default=genID,null=False,primary_key=True)
    fname = models.CharField(max_length=64, null=False)
    lname = models.CharField(max_length=64, null=False)
    email = models.EmailField(null=False,unique=True)
    password = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=200, null=False)
    tel = models.CharField(max_length=10, null=False,unique=True)

    def fullname(self):
        return self.fname + " " + self.lname

class Promotion_type(models.Model):
    promotion_code = models.CharField(max_length=7, null=False, primary_key=True)
    promotion_name = models.CharField(max_length=32, null=False)
    promotion_detail = models.CharField(max_length=500, null = False)
    start_date = models.DateField(null=False)
    expire_date = models.DateField(null= False)
    discount = models.FloatField(null=False)

    def __str__(self) :
        return self.promotion_name

class Room_booking(models.Model):
    def bhID():
        n = Room_booking.objects.count()
        if n == 0:
            return "BH00000001"
        else:
            return "BH" + str(n+1).zfill(9)
    booking_no = models.CharField(max_length=11,default=bhID, null=False, primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE, null=False)
    date_check_in = models.DateTimeField(null = False)
    date_check_out = models.DateTimeField(null=False)
    promotion_code = models.ForeignKey(Promotion_type, on_delete=models.SET_NULL, null=True)
    number_guest = models.IntegerField(null=False)
    total_charge = models.FloatField(null=False)
    payment_method = models.CharField(max_length=32)

    #try query data
    def __str__(self) :
        return self.date_check_in

class Room_type(models.Model):
    roomtype = models.CharField(max_length=30, null=False, primary_key=True)
    capacity = models.IntegerField(null = False)
    price = models.FloatField(null=False)

    #try query data   
    def __str__(self) :
        return self.roomtype


class Room_available(models.Model):
    room_no = models.CharField(max_length=4,null=False, primary_key=True)
    roomtype = models.ForeignKey(Room_type, on_delete=models.CASCADE, null=False)
    status = models.BooleanField(null=False)

class Service(models.Model):
    service_code = models.CharField(max_length=10, null=False, primary_key=True)
    service_name = models.CharField(max_length=20, null = False,unique=True)
    charge = models.FloatField(null = True)

    #try query data    
    def __str__(self) :
        return self.service_name
    

class Room_detail(models.Model):
    booking_no = models.ForeignKey(Room_booking, on_delete=models.RESTRICT, null=False)
    room_no = models.ForeignKey(Room_available, on_delete=models.CASCADE, null=False)
    service_code = models.ForeignKey(Service, on_delete = models.CASCADE, null=True)
    service_count = models.IntegerField(null=False)
    
class Resbooking(models.Model):
    def brID():
        n = Resbooking.objects.count()
        if n == 0:
            return "BR00000001"
        else:
            return "BR" + str(n+1).zfill(9)

    resb_no = models.CharField(max_length=11,default= brID ,null=False,unique=True, primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE, null=False)
    promotion_code = models.ForeignKey(Promotion_type, on_delete=models.SET_NULL, null=True)
    number_guest = models.IntegerField(null=False)
    total_charge = models.FloatField(null=False)
    payment_method = models.CharField(max_length=32)

class Buffet_round(models.Model):
    round = (('lunch',"LUNCH"),('dinner',"DINNER"))
    buffet_round=models.CharField(max_length=64,choices=round,default=False ,null=False)
    charge=models.FloatField(null =True)

class Buffet_table(models.Model):
    table_no = models.IntegerField(null=False)
    buffet_round = models.ForeignKey(Buffet_round, on_delete=models.CASCADE, null=False)
    status = models.BooleanField(null = False)

class Resb_detail(models.Model):
    resb_no = models.ForeignKey(Resbooking, on_delete=models.RESTRICT, null=False)
    table_no = models.ForeignKey(Buffet_table, on_delete=models.CASCADE, null=False)

class Customer_booking(models.Model):   
    customer_id = models.ForeignKey(Customer, on_delete=models.RESTRICT, null=False)
    booking_no = models.ForeignKey(Room_booking,on_delete=models.RESTRICT, null=True)
    resb_no = models.ForeignKey(Resbooking, on_delete=models.RESTRICT, null=True)
    booking_date = models.DateTimeField(auto_now_add=True, null=False)

class Invoice(models.Model):
    invoice_no = models.CharField(max_length=12, null=False, primary_key=True, unique=True)
    booking_no = models.ForeignKey(Room_booking, on_delete=models.RESTRICT, null=True)
    resb_no = models.ForeignKey(Resbooking, on_delete = models.RESTRICT, null=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.RESTRICT, null=False)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE, null=False)
    tax = models.FloatField(null=False)
    date = models.DateField(null=False)


