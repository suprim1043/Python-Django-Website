from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()
import uuid

class HomepageForm(forms.ModelForm):
    class Meta():
       model = Homepage_Slider
       fields = '__all__'
       app_label = "User"


class UserForm(UserCreationForm):
    class Meta:
        model = User
        first_name = forms.CharField()
        last_name = forms.CharField()
        fields = ['first_name','last_name','email','password1','password2']
        widgets = {
            'email':forms.EmailInput(attrs = {'autocomplete':'off'}),
            'password1':forms.PasswordInput(attrs = {'autocomplete':'new-password'}),
            'password2':forms.PasswordInput(attrs = {'autocomplete':'off'}),
        }
        def clean(self):
            self.email = self.capitalize()

class ContactForm(forms.ModelForm):
    class Meta():
        model = ContactModel
        fields = "__all__"


class ReviewForm(forms.ModelForm):
    class Meta():
        model = Reviews
        fields = ['Email','Name','Text','Image1',"Image2"]


