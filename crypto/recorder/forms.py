from django.forms import ModelForm,Form
from django import forms
from django.contrib.auth.models import User

class SignupForm(ModelForm):
    username=forms.CharField(max_length=50,widget=forms.TextInput(attrs={"placeholder":"username","class":"form-control p-2"}))
    email=forms.CharField(max_length=50,widget=forms.EmailInput(attrs={"placeholder":"email","class":"form-control p-2"}))
    password=forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={"placeholder":"password","class":"form-control p-2"}))
    
    class Meta:
        model=User
        fields=["username","email","password"]

class LoginForm(Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={"placeholder":"Enter Email or username","class":"form-control p-2"}))
    password=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={"placeholder":"Password","class":"form-control p-2"}))