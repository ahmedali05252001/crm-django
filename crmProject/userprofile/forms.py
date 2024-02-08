from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


INPUT_CLASS = "mb-4 w-full my-4 py-4 px-6 rounded-xl bg-gray-100" 

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget= forms.TextInput(attrs={
        "placeholder" : "Your username",
        "class" : INPUT_CLASS 
    }))
    password = forms.CharField(widget= forms.PasswordInput(attrs={
        "placeholder" : "Your password",
        "class" : INPUT_CLASS 
    }))
    

class SignupForm(UserCreationForm):
    username = forms.CharField(widget= forms.TextInput(attrs={
        "placeholder" : "Your username",
        "class" : INPUT_CLASS 
    }))
    email = forms.CharField(widget= forms.EmailInput(attrs={
        "placeholder" : "Your email addres",
        "class" : INPUT_CLASS 
    }))
    password1 = forms.CharField(widget= forms.PasswordInput(attrs={
        "placeholder" : "Your password",
        "class" : INPUT_CLASS 
    }))
    password2 = forms.CharField(widget= forms.PasswordInput(attrs={
        "placeholder" : "Repeat password",
        "class" : INPUT_CLASS 
    }))