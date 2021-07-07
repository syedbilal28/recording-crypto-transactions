from django.urls import path
from . import views
urlpatterns=[
    path("signup/",views.signup,name="Signup"),
    path("",views.Login,name="Login"),
    path("purchase/",views.purchase,name="Purchase"),
    path('add-product/',views.AddProduct,name="Addproduct"),
    path("sales/",views.sale,name="Sales"),
    path("report/<str:product_id>/",views.report,name="Report"),
    path("gas-fee/",views.gasfee,name="GasFee"),
    path("transactions/",views.transactions,name="Transaction"),
    path("administrator/",views.admin,name="Admin"),
    path("email/",views.email,name="Email"),
    path("transaction/<str:transaction_id>/",views.TransactionData,name="TransactionData"),
    path("edit-transaction/",views.EditTransaction,name="EditTransaction"),
    path("transactions-filter/<str:filter>/",views.TransactionsFilter,name="TransactionFilter")
]