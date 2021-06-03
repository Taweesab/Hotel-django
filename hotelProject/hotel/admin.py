from django.contrib import admin
from .models import *

# Register your models here.
#### try model #########
admin.site.register(staff)
admin.site.register(customer)
admin.site.register(customer_booking)
admin.site.register(promotion_type)
admin.site.register(room_booking)
admin.site.register(room_type)
admin.site.register(room_available)
admin.site.register(service)
admin.site.register(room_detail)
admin.site.register(resbooking)
admin.site.register(buffet_round)
admin.site.register(buffet_table)
admin.site.register(resb_detail)
admin.site.register(invoice)


