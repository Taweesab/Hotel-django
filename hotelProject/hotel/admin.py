from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(promotion_type)
#### try model #########
admin.site.register(room_booking)
admin.site.register(room_type)
admin.site.register(service)
admin.site.register(staff)
admin.site.register(customer)
admin.site.register(customer_booking)


