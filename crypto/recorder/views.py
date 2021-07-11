
from django.http.response import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from .forms import GasFeeForm, ProductForm, SignupForm,LoginForm,PurchaseForm,SaleForm
from django.contrib.auth import login, logout,authenticate
from .calculator import ProfitCalculator
from .models import Transaction,Product,GasFee,Inventory,Suggestion,Upvote,Downvote,ChatMessage,Thread
from datetime import datetime,date
from django.contrib.auth.models import User
import copy
from .serializers import ChatMessageSerializer, SuggestionSerializer, TransactionSerializer,ProductSerializer,GasFeeSerializer,ThreadSerializer,UserSerializer
import calendar
from django.views.decorators.csrf import csrf_exempt
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
    if request.user.is_authenticated:
        return redirect("Purchase")
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
        print(request.POST.get("form"))
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
        transaction=TransactionSerializer(transaction).data
        return JsonResponse({"transaction":transaction},status=200)
        # print(request.POST)
        # print(form.is_valid())
        # if form.is_valid():
        #     form.save()
            
    else:
        form=PurchaseForm()
        context={"form":form}
        return render(request,"purchases.html",context)

def AddProduct(request):
    print(request.POST,request.FILES)
    if request.method=="POST":
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product=form.save()
            
        # return redirect("Purchase")
            product=ProductSerializer(product).data
            return JsonResponse({"product":product},status=201)
        
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
            form= SaleForm()
            context={"form":form,"message":"You do not have this product available"}
            return render(request,"sales.html",context)
            # return JsonResponse({"message":"You do not have this product available"},status=400)
        
        
        if inventory.available_quantity < int(data['quantity']):
            # return JsonResponse({"message":"You do not have enough resources"},status=400)
            form= SaleForm()
            context={"form":form,"message":"You do not have enough resources"}
            return render(request,"sales.html",context)
        
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
        # return HttpResponse("Hello Worls")
        product=Product.objects.get(pk=int(data['product']))
        return redirect(f"/report/{product.pk}/")
        # try:
        #     inventory=Inventory.objects.get(user=request.user,product=)
    else:
        form= SaleForm()
        context={"form":form}
        return render(request,"sales.html",context)

def report(request,product_id):
    try:
        product= Product.objects.get(pk=int(product_id))
    except:
        return redirect("/report/1/")

    transactions_sp= Transaction.objects.filter(user=request.user,product=product)  
    profit=ProfitCalculator(transactions_sp)
    transactions=transactions_sp.filter(Type="sale")
    if len(profit)>0:
        overall_profit=round(((profit[0].sales-profit[0].purchase)/profit[0].purchase)*100,3)
    else:
        overall_profit=0
    

    all_transactions= Transaction.objects.filter(user=request.user)
    profits=ProfitCalculator(all_transactions)
    print(profits)
    transaction_with_profits=[]
    for i in profits:
        temp=((i.sales-i.purchase)/i.purchase)*100
        if temp <0:
            temp=0
        transaction_with_profits.append(temp)
        # transaction_with_profits[i.name]= [i.purchase,i.sales] 
    profits=sorted(transaction_with_profits,reverse=True)
    profits=profits[0:4]
    # for i in sales:
    x_data=[i.timestamp.strftime("%d-%m-%Y") for i in transactions]
    y_data=[i.profit for i in transactions]
    context={"x":x_data,"y":y_data,"product":product,"tr_profits":profits,"ov_profit":overall_profit}
    return render(request,"report.html",context)

def base(request):
    return render(request,"base.html")

def gasfee(request):
    print(request.POST)
    if request.method=="POST":
        form=GasFeeForm(request.POST)
        if form.is_valid():
            gas_fee=form.save()
            
            # gas_fee=GasFeeSerializer(gas_fee).data
            return redirect(gasfee)
            # return JsonResponse({"gasfee":gas_fee},status=201)
    else:
        gasfees=GasFee.objects.all()
        fees=[]
        for i in gasfees:
            fees.append(i.fee)
        try:
            avg= round(sum(fees)/len(fees),4)
        except:
            avg=0
        overall=round(sum(fees),4)
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
    transactions=Transaction.objects.filter(user=request.user)
    context={"transactions":transactions}
    return render(request,"transaction.html",context)
def DeleteTransaction(request,transaction_id):
    transaction=Transaction.objects.get(pk=int(transaction_id))
    transaction.delete()
    return JsonResponse({"id":transaction_id},status=200)

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
    if filter =="purchase" or filter=="sale":
        transactions=Transaction.objects.filter(Type=filter,user=request.user)
    else:
        transactions=Transaction.objects.filter(user=request.user)
    
    transactions=TransactionSerializer(transactions,many=True).data
    return JsonResponse({"transactions":transactions},status=200)

def suggestions(request):
    
    return render(request,"suggestions.html")

def SuggestionsAPI(request):
    suggestions= Suggestion.objects.all()
    suggestions=SuggestionSerializer(suggestions,many=True).data
    return JsonResponse({"suggestions":suggestions},status=200)
def like(request,suggestion_id):
    suggestion=Suggestion.objects.get(pk=int(suggestion_id))
    print(request.user)
    like=suggestion.like(request.user)
    if like:
        return JsonResponse({"message":"liked"})
    return JsonResponse({"message":"disliked"})
def upvote(request,suggestion_id):
    suggestion=Suggestion.objects.get(pk=int(suggestion_id))
    vote=suggestion.upvote(request.user)
    upvotes=Upvote.objects.filter(suggestion=suggestion).count()
    downvotes=Downvote.objects.filter(suggestion=suggestion).count()    
    if vote:
        return JsonResponse({"message":"upvoted","upvotes":upvotes,"downvotes":downvotes})
    return HttpResponse(status=406)

def downvote(request,suggestion_id):
    suggestion=Suggestion.objects.get(pk=int(suggestion_id))
    vote=suggestion.downvote(request.user)
    upvotes=Upvote.objects.filter(suggestion=suggestion).count()
    downvotes=Downvote.objects.filter(suggestion=suggestion).count()
    return JsonResponse({"message":"downvoted","upvotes":upvotes,"downvotes":downvotes})
       
def admin(request):
    if request.user.is_superuser:
        
        return render(request,"admin_home.html")
    return redirect("Purchase")

def ActivitiesApi(request):
    activities= Transaction.objects.all().reverse()[:3]
    activities=TransactionSerializer(activities,many=True).data
    return JsonResponse({"activities":activities},status=200)
def UsersApi(request):
    users=User.objects.all()
    users=UserSerializer(users,many=True).data
    return JsonResponse({"users":users},status=200)

def ThreadsApi(request):
    threads=Thread.objects.all()[:4]
    threads=ThreadSerializer(threads,many=True).data
    return JsonResponse({"threads":threads},status=200)

@csrf_exempt
def chatApi(request):
    admin= User.objects.filter(is_staff=True)[0]
    thread=Thread.objects.get_or_new(user=admin,other_username=request.user)[0]
    print(thread)
    messages=ThreadSerializer(thread).data
    return JsonResponse({"thread":messages},status=200)

def ChatApiAdmin(request,username):
    thread=Thread.objects.get_or_new(user=request.user,other_username=User.objects.get(username=username))[0]
    print(thread)
    messages=ThreadSerializer(thread).data
    return JsonResponse({"thread":messages},status=200)

@csrf_exempt
def SendMessage(request):
    if request.POST.get("other_user"):
        admin=request.user    
        user=User.objects.get(username=request.POST.get("other_user"))
    else:    
        admin= User.objects.filter(is_staff=True)[0]
        user=request.user
    thread=Thread.objects.get_or_new(user=admin,other_username=user)[0]
    msg=ChatMessage.objects.create(thread=thread,message=request.POST.get("message"),user=request.user)
    msg_serialized=ChatMessageSerializer(msg).data
    return JsonResponse({"message":msg_serialized},status=200)

def email(request):
    return render(request,"admin_email.html")