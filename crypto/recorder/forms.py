from django.forms import ModelForm,Form
from django import forms
from django.contrib.auth.models import User
from .models import Product, Transaction
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

class ProductForm(ModelForm):
    # name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={"class":"choice","id":"pname"}))
    # collection=forms.CharField(max_length=50,widget=Select)
    class Meta:
        model=Product   
        fields="__all__"

class PurchaseForm(ModelForm):
    note=forms.CharField(max_length=200,widget=forms.Textarea(attrs={"class":"get form-control quarter","col":"30","rows":"5"}))
    price=forms.IntegerField(widget=forms.NumberInput(attrs={"class":"get form-control more-half"}))
    qunatity=forms.IntegerField(widget=forms.NumberInput(attrs={"class":"get form-control more-half"}))
    timestamp=forms.DateField(widget=forms.DateInput(attrs={"class":"get form-control half"}))
    class Meta:
        model=Transaction
        fields="__all__"

