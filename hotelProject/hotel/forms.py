from django.forms import ModelForm, fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import DateInput
from .models import Staff


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