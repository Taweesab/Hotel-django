# from hotelProject.hotel.models import room_booking
from django.forms import ModelForm, fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import DateInput
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

# class bookhotel(ModelForm) :
#     class Meta:
#         model = room_booking
#         fields = ['date_check_in','date_check_out','promotion_code','number_guest','total_charge','payment_method']

