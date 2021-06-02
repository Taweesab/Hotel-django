from os import name
from django.db import models

# Create your models here.
class staff(models.Model):
    staff_id = models.CharField(max_length=9, null= False)
    fname = models.CharField(max_length=64, null=False)
    lname = models.CharField(max_length=64, null=False)
    dob = models.DateField(null=False)
    job_title = models.CharField(max_length=64, null=False)
    salary = models.FloatField(null=False)
    email = models.EmailField(null=False)
    password = models.CharField(max_length=100, null=False)

class customer(models.Model):
    customer_id = models.CharField(max_length=11, null=False)
    fname = models.CharField(max_length=64, null=False)
    lname = models.CharField(max_length=64, null=False)
    email = models.EmailField(null=False)
    password = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=200, null=False)
    tel = models.CharField(max_length=10, null=False)

    def fullName(self):
        return self.fName + " " + self.lName

class customer_booking(models.Model):
    customer_id = models.ForeignKey(customer, on_delete=models.RESTRICT, null=False)
    booking_no = models.CharField(max_length=11, null=True)
    resb_no = models.CharField(max_length=11, null=True)
    booking_date = models.DateTimeField(auto_now_add=True, null=False)

class promotion_type(models.Model):
    promotion_code = models.CharField(max_length=7, null=False)
    promotion_name = models.CharField(max_length=32, null=False)
    promotion_detail = models.CharField(max_length=500, null = False)
    start_date = models.DateField(null=False)
    expire_date = models.DateField(null= False)
    discount = models.FloatField(null=False)

    def __str__(self) :
        return self.promotion_name

class room_booking(models.Model):
    booking_no = models.ForeignKey(customer_booking, on_delete=models.RESTRICT, null=False)
    staff_id = models.ForeignKey(staff, on_delete=models.CASCADE, null=False)
    date_check_in = models.DateTimeField(null = False)
    date_check_out = models.DateTimeField(null=False)
    promotion_code = models.ForeignKey(promotion_type, on_delete=models.SET_NULL, null=True)
    number_guest = models.IntegerField(null=False)
    total_charge = models.FloatField(null=False)
    payment_method = models.CharField(max_length=32)
    #wait for payment page

class room_type(models.Model):
    roomtype = models.CharField(max_length=30, null=False)
    capacity = models.IntegerField(null = False)
    price = models.FloatField(null=False)

class room_available(models.Model):
    room_no = models.CharField(max_length=4,null=False)
    roomtype = models.ForeignKey(room_type, on_delete=models.CASCADE, null=False)
    status = models.BooleanField(null=False)

class service(models.Model):
    service_code = models.CharField(max_length=10, null=False)
    service_name = models.CharField(max_length=20, null = False)
    charge = models.FloatField(null = True)

class room_detail(models.Model):
    booking_no = models.ForeignKey(room_booking, on_delete=models.RESTRICT, null=False)
    room_no = models.ForeignKey(room_available, on_delete=models.CASCADE, null=False)
    service_code = models.ForeignKey(service, on_delete = models.CASCADE, null=True)
    service_count = models.IntegerField(null=False)
    
class resbooking(models.Model):
    resb_no = models.ForeignKey(customer_booking, on_delete=models.RESTRICT, null=False)
    staff_id = models.ForeignKey(staff, on_delete=models.CASCADE, null=False)
    promotion_code = models.ForeignKey(promotion_type, on_delete=models.SET_NULL, null=True)
    number_guest = models.IntegerField(null=False)
    total_charge = models.FloatField(null=False)
    payment_method = models.CharField(max_length=32)
    #wait for payment page

class buffet_round(models.Model):
    buffet_round=models.CharField(max_length=64, null=False)
    charge=models.FloatField(null =True)

class buffet_table(models.Model):
    table_no = models.IntegerField(null=False)
    buffet_round = models.ForeignKey(buffet_round, on_delete=models.CASCADE, null=False)
    status = models.BooleanField(null = False)

class resb_detail(models.Model):
    resb_no = models.ForeignKey(resbooking, on_delete=models.RESTRICT, null=False)
    table_no = models.ForeignKey(buffet_table, on_delete=models.CASCADE, null=False)

class invoice(models.Model):
    invoice_no = models.CharField(max_length=12, null=False)
    booking_no = models.ForeignKey(room_booking, on_delete=models.RESTRICT, null=True)
    resb_no = models.ForeignKey(resbooking, on_delete = models.RESTRICT, null=True)
    customer_id = models.ForeignKey(customer, on_delete=models.RESTRICT, null=False)
    staff_id = models.ForeignKey(staff, on_delete=models.CASCADE, null=False)
    tax = models.FloatField(null=False)
    date = models.DateField(null=False)