from django.contrib import admin
from .models import *

# Register your models here.
#### try model #########
admin.site.register(Staff)
admin.site.register(Customer)
admin.site.register(Customer_booking)
admin.site.register(Promotion_type)
admin.site.register(Room_booking)
admin.site.register(Room_type)
admin.site.register(Room_available)
admin.site.register(Service)
admin.site.register(Room_detail)
admin.site.register(Resbooking)
admin.site.register(Buffet_round)
admin.site.register(Buffet_table)
admin.site.register(Resb_detail)
admin.site.register(Invoice)


