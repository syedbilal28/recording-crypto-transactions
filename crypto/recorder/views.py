from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from .forms import ProductForm, SignupForm,LoginForm,PurchaseForm,SaleForm
from django.contrib.auth import login, logout,authenticate
from .models import Transaction,Product
from datetime import datetime
# Create your views here.
def signup(request):
    if request.method== "POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("Login")
    else:
        form=SignupForm()
        return render(request,"signup.html",{"form":form})

def Login(request):
    if request.method=="POST":
        form= LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                
            else:
                form=LoginForm()
                return render(request,"login.html",{"form":form,"message":"incorrect credentials"})        

    else:
        form=LoginForm()
        return render(request,"login.html",{"form":form})

def purchase(request):
    if request.method=="POST":
        form=PurchaseForm(request.POST)
        data=request.POST
        print(data)
        transaction=Transaction.objects.create(
            product=Product.objects.get(pk=int(data['product'])),
            price=int(data['price']),
            Type=data['Type'],
            quantity=int(data['quantity']),
            timestamp=datetime.strptime(data['timestamp'],'%Y-%m-%d').date(),
            note=data['note']
        )
        # print(request.POST)
        # print(form.is_valid())
        # if form.is_valid():
        #     form.save()
            
    else:
        form=PurchaseForm()
        context={"form":form}
        return render(request,"purchases.html",context)

def AddProduct(request):
    if request.method=="POST":
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    else:
        form=ProductForm()
        context={"form":form}
        return render(request,"add-product.html",context)
def sale(request):
    if request.method == "POST":
        pass
    else:
        form= SaleForm()
        context={"form":form}
        return render(request,"sales.html",context)