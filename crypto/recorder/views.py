
from django.http.response import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from .forms import GasFeeForm, ProductForm, SignupForm,LoginForm,PurchaseForm,SaleForm
from django.contrib.auth import login, logout,authenticate
# from .authentication_email.
from .models import Transaction,Product,GasFee,Inventory
from datetime import datetime,date
import copy
from .serializers import TransactionSerializer,ProductSerializer
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
            print(username)
            password=form.cleaned_data["password"]
            user=authenticate(request,username=username,password=password)
            # if not user:
            #     user=authenticate(request,email=username,password=password)
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
            user=request.user,
            product=Product.objects.get(pk=int(data['product'])),
            price=int(data['price']),
            Type=data['Type'],
            quantity=int(data['quantity']),
            timestamp=datetime.strptime(data['timestamp'],'%Y-%m-%d').date(),
            note=data['note']
        )
        try:
            inventory= Inventory.objects.get(user=request.user,product=transaction.product)
        except:
            inventory= Inventory.objects.create(
                user=request.user,
                product=transaction.product
            )
        inventory.available_quantity+=int(data['quantity'])
        inventory.save()
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
        try:
            inventory= Inventory.objects.get(user=request.user,product=Product.objects.get(pk=int(data['product'])))
        except:
            return JsonResponse({"message":"You do not have this product available"},status=400)
        
        
        if inventory.available_quantity < int(data['quantity']):
            return JsonResponse({"message":"You do not have enough resources"},status=400)
        
        transaction=Transaction.objects.create(
            user=request.user,
            product=Product.objects.get(pk=int(data['product'])),
            price=int(data['price']),
            Type=data['Type'],
            quantity=int(data['quantity']),
            timestamp=date.today(),
            percentage= float(data["percentage"])
        )
        previous_transactions= Transaction.objects.filter(user=transaction.user,Type="purchase")
        print(previous_transactions)
        available_units= Inventory.objects.filter(user=transaction.user,product=transaction.product)[0].available_quantity
        print(available_units)
        num=0
        available_products=[]
        for i in previous_transactions:
            if num < available_units:
                num+=i.quantity
                available_products.append(copy.deepcopy(i))
                if num >= available_units:
                    available_products[-1].quantity-=(num-available_units)
                    cost=CalculateCost(available_products,transaction.quantity) 
                    print("calculating profit")
                    profit=transaction.price-cost

                    transaction.profit= profit
                    print("Put profit")
                    transaction.save()
            else:
                break

        inventory.available_quantity-=int(data['quantity'])
        inventory.save()
        return HttpResponse("Hello Worls")
        # try:
        #     inventory=Inventory.objects.get(user=request.user,product=)
    else:
        form= SaleForm()
        context={"form":form}
        return render(request,"sales.html",context)

def report(request,product_id):
    product= Product.objects.get(pk=int(product_id))
    transactions= Transaction.objects.filter(user=request.user,product=product,Type="sale")  
    # for i in sales:
    x_data=[i.timestamp.strftime("%d-%m-%Y") for i in transactions]
    y_data=[i.profit for i in transactions]
    context={"x":x_data,"y":y_data}
    return render(request,"report.html",context)

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

def transactions(request):
    transactions=Transaction.objects.all()
    context={"transactions":transactions}
    return render(request,"transaction.html",context)

def CalculateCost(available_products,quantity):
    cost=0
    count=0
    for i in available_products:
        if count< quantity:
            cost+=i.price
            count+=i.quantity
        if count> quantity:
            cost_per_piece= i.quantity/i.price 
            cost-= ((count-quantity)*cost_per_piece)
            
            break
    return cost

def TransactionData(request,transaction_id):
    transaction=Transaction.objects.get(pk=int(transaction_id))
    transaction=TransactionSerializer(transaction).data
    products= Product.objects.all()
    products=ProductSerializer(products,many=True).data
    return JsonResponse({"transaction":transaction,"products":products},status=200)
def EditTransaction(request):
    print(request.POST)
    if request.method=="POST":
        pk=request.POST.get("pk")
        product=request.POST.get("product") 
        product= Product.objects.get(pk=int(product))
        price=int(request.POST.get("price"))
        quantity=int(request.POST.get("quantity"))
        date=datetime.strptime(request.POST.get("date"),"%Y-%m-%d").date()
        transaction= Transaction.objects.get(pk=int(pk))
        transaction.product=product
        transaction.price=price
        transaction.quantity=quantity
        transaction.timestamp=date
        transaction.save()
        transaction=TransactionSerializer(transaction).data
        return JsonResponse({"transaction":transaction},status=200)
    return HttpResponse(status=200)

def TransactionsFilter(request,filter):
    if filter:
        transactions=Transaction.objects.filter(Type=filter,user=request.user)
    else:
        transactions=Transaction.objects.filter(user=request.user)
    transactions=TransactionSerializer(transactions,many=True).data
    return JsonResponse(transactions,status=200)
def admin(request):
    return render(request,"admin_home.html")

def email(request):
    return render(request,"admin_email.html")