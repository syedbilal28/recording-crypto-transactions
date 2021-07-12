from django.forms import ModelForm,Form
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import NumberInput
from .models import Product, Transaction,GasFee,EmailMessage
from django.core.mail import send_mail
from crypto.settings import EMAIL_HOST_USER
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
    quantity=forms.IntegerField(widget=forms.NumberInput(attrs={"class":"get form-control more-half"}))
    timestamp=forms.DateField(widget=forms.DateInput(attrs={"class":"get form-control half"}))
    Type=forms.CharField(max_length=50,widget=forms.TextInput(attrs={"value":"purchase"}))
    class Meta:
        model=Transaction
        fields="__all__"

class SaleForm(ModelForm):
    note=forms.CharField(max_length=200,widget=forms.Textarea(attrs={"class":"get form-control quarter","col":"30","rows":"5"}))
    price=forms.IntegerField(widget=forms.NumberInput(attrs={"class":"get form-control more-half extra-rounded"}))
    quantity=forms.IntegerField(widget=forms.NumberInput(attrs={"class":"get form-control half extra-rounded"}))
    timestamp=forms.DateField(widget=forms.DateInput(attrs={"class":"get form-control half extra-rounded"}))
    Type=forms.CharField(max_length=50,widget=forms.TextInput(attrs={"value":"sale"}))
    # product=forms.CharField(max_length=50,widget=forms.TextInput(attrs={"class":"get form-control half"}))
    percentage=forms.FloatField(widget=NumberInput(attrs={"class":"get form-control more-half extra-rounded"}))
    class Meta:
        model=Transaction
        fields="__all__"

class GasFeeForm(ModelForm):
    fee= forms.FloatField(widget=NumberInput(attrs={"placeholder":0.001}))
    class Meta:
        model=GasFee
        fields="__all__"

class ContactForm(forms.Form):
    name=forms.CharField(max_length=200,widget=forms.TextInput(attrs={"class":"form-control p-2","placeholder":"Your Name"}))
    email=forms.EmailField(max_length=200,widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"Your Email"}))
    message=forms.CharField(max_length=1500,widget=forms.Textarea(attrs={"class":"form-control p-2","placeholder":"Your Message"}))

    def save(self,commit=False):
        subject=f"Message from {self.cleaned_data['name']} with email address {self.cleaned_data['email']}"
        message=self.cleaned_data["message"]
        recepient="syed.bilal.sba@gmail.com"
        send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        email=EmailMessage.objects.create(
            name=self.cleaned_data["name"],
            email=self.cleaned_data["email"],
            message=self.cleaned_data["message"]
        )

        return email
