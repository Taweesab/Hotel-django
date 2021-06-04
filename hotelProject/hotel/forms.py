from django.forms import ModelForm, fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import DateInput
from .models import *


class bookhotel(forms.Form) :
    checkin = forms.DateField(widget=DateInput)
    

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password1','password2']
        

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'

class CustomerRegisterForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['customer_id']
    def __init__(self,*args,**kwargs):
        super(CustomerRegisterForm, self).__init__(*args,**kwargs)
        self.fields['fname'].error_messages = {'required': 'Please enter your first name',}
        self.fields['lname'].error_messages = {'required': 'Please enter your last name',}
        self.fields['email'].error_messages = {'required': 'Please enter your e-mail','invalid': 'This e-mail is used',}
        self.fields['tel'].error_messages = {'required': 'Please enter your telphone','invalid': 'Please enter a valid telphone',}

class RestBookingForm(forms.ModelForm):
    class Meta:
        model = Resbooking
        exclude = ['resb_no']
