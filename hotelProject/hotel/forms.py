# from hotelProject.hotel.models import room_booking
from django.forms import ModelForm, fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
from .models import Room_booking


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password1','password2']
        

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ['staff_id','salary','job_title']

class CustomerRegisterForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['customer_id']
    def __init__(self,*args,**kwargs):
        super(CustomerRegisterForm, self).__init__(*args,**kwargs)
        self.fields['fname'].info_messages = {'required': 'Please enter your first name',}
        self.fields['lname'].info_messages = {'required': 'Please enter your last name',}
        self.fields['email'].info_messages = {'required': 'Please enter your e-mail','invalid': 'This e-mail is used',}
        self.fields['tel'].info_messages = {'required': 'Please enter your telphone','invalid': 'Please enter a valid telphone',}

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['customer_id','password']

class RestBookingForm(forms.ModelForm):
    class Meta:
        model = Resbooking
        # fields = '__all__'
        exclude = ['resb_no'] 

class CustomerBookingForm(forms.ModelForm):
    class Meta:
        model = Customer_booking
        exclude = ['no','booking_no'] 

class CustomerHotelForm(forms.ModelForm):
    class Meta:
        model = Customer_booking
        exclude = ['no','resb_no'] 

class HotelbookingForm(forms.ModelForm) :
    class Meta :
        model = Room_booking
        exclude = ['bhsurrogate','booking_no','detail_no']
        # fields = '__all__'

class RoomdetailForm(forms.ModelForm) :
    class Meta :
        model = Room_detail
        exclude = ['detail_no']
        # fields = '__all__'

class Editroombooking(forms.ModelForm):
    class Meta :
        model = Room_booking
        exclude = ['date_check_in', 'date_check_out', 'payment_method' , 'promotion_code','booking_no']

class Editresbooking(forms.ModelForm):
    class Meta :
        model = Resbooking
        exclude = ['resb_no', 'eatdate', 'paymentmethod' , 'promotion_code']

class InvoiceHotelForm(forms.ModelForm) :
    class Meta :
        model = Invoice
        exclude = ['resb_no']

class InvoiceRestaurantForm(forms.ModelForm) :
    class Meta :
        model = Invoice
        exclude = ['booking_no']












