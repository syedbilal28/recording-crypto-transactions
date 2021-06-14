from django.urls import path
from . import views
urlpatterns=[
    path("signup/",views.signup,name="Signup"),
    path("",views.Login,name="Login"),
    path("purchase/",views.purchase,name="Purchase")
]