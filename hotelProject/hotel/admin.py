from django.contrib import admin
from .models import *

# Register your models here.
#### try model #########
class Admin_Staff(admin.ModelAdmin):
    list_display=["staff_id","fname","lname","job_title"]
    search_fields=["staff_id","fname","lname","job_title"]
    list_filter=["job_title"]
 

class Admin_Customer(admin.ModelAdmin):
    list_display=["customer_id","fname","lname"]
    search_fields=["fname","lname"]


class Admin_Promo(admin.ModelAdmin):
    list_display=["promotion_code","promotion_name","promotion_type","start_date","expire_date"]
    search_fields=["promotion_code","promotion_name"]
    list_filter=["promotion_type"]


class Admin_Room(admin.ModelAdmin):
    list_display=["roomtype","capacity","price"]
    list_filter=["roomtype"]


class Admin_Service(admin.ModelAdmin):
    list_display=["service_code","service_name","charge"]


class Admin_RoomDe(admin.ModelAdmin):
    list_display=["detail_no","roomtype","service_name","room_count"]


class Admin_BH(admin.ModelAdmin):
    list_display=["bhsurrogate","booking_no","detail_no","date_check_in","date_check_out","number_guest"]
    search_fields=["booking_no"]


class Admin_Buffet(admin.ModelAdmin):
    list_display=["buffet_round","charge","amount"]


class Admin_BR(admin.ModelAdmin):
    list_display=["resb_no","number_guest","eatdate","buffet_round"]
    search_fields=["resb_no"]
    

class Admin_CusBook(admin.ModelAdmin):
    list_display=["no","customer_id","booking_no","resb_no","booking_date"]
    list_filter=["customer_id"]
    

class Admin_Invoice(admin.ModelAdmin):
    list_display=["invoice_no","customer_id","staff_id","tax","date"]
    list_filter=["staff_id"]
    search_fields=["invoice_no","customer_id","staff_id"]

admin.site.register(Staff,Admin_Staff)
admin.site.register(Customer,Admin_Customer)
admin.site.register(Promotion_type,Admin_Promo)
admin.site.register(Room,Admin_Room)
admin.site.register(Service,Admin_Service)
admin.site.register(Room_detail,Admin_RoomDe)
admin.site.register(Room_booking,Admin_BH)
admin.site.register(Resbooking,Admin_BR)
admin.site.register(Buffet_round,Admin_Buffet)
admin.site.register(Customer_booking,Admin_CusBook)
admin.site.register(Invoice,Admin_Invoice)

#Admin Header
admin.site.site_header = "Boiled-Youtiao Administration"