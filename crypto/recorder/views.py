from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from .forms import GasFeeForm, ProductForm, SignupForm,LoginForm,PurchaseForm,SaleForm
from django.contrib.auth import login, logout,authenticate
from .models import Transaction,Product,GasFee
from datetime import datetime,date

import calendar

# Create your views here.
def signup(request):
    if request.method== "POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(form.cleaned_data["password"])
            user.save()
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
                return redirect("Purchase")
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
        return redirect("Purchase")
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
        form=SaleForm(request.POST)
        data=request.POST
        print(data)
        transaction=Transaction.objects.create(
            product=Product.objects.get(pk=int(data['product'])),
            price=int(data['price']),
            Type=data['Type'],
            quantity=int(data['quantity']),
            
            
        )
    else:
        form= SaleForm()
        context={"form":form}
        return render(request,"sales.html",context)

def report(request,product_id):
    product= Product.objects.get(pk=int(product_id))
    transactions= Transaction.objects.filter(product=product)
    purchases= transactions.filter(Type="purchase")
    sales= transactions.filter(Type="sale")
    
    return render(request,"report.html")

def base(request):
    return render(request,"base.html")

def gasfee(request):
    if request.method=="POST":
        form=GasFeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(gasfee)
    else:
        gasfees=GasFee.objects.all()
        fees=[]
        for i in gasfees:
            fees.append(i.fee)
        try:
            avg= sum(fees)/len(fees)
        except:
            avg=0
        overall=sum(fees)
        x_data=[i.date.strftime("%d-%m-%Y") for i in gasfees]
        y_data=[i.fee for i in gasfees ]
        form=GasFeeForm()
        
        current=date.today().month
        prev_1=calendar.month_name[current-1]
        prev_2=calendar.month_name[current-2]
        prev_3=calendar.month_name[current-3]
        year=date.today().year

        context={"form":form,"average":avg,"overall":overall,"x":x_data,"y":y_data,"prev_1":prev_1,"prev_2":prev_2,"prev_3":prev_3,"year":year}
        return render(request,"gas-fee.html",context)