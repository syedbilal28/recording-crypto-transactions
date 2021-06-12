from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from .forms import SignupForm,LoginForm
from django.contrib.auth import login, logout,authenticate
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