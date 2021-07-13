from django.contrib.auth import logout
from django.urls import path
from . import views
urlpatterns=[
    path("",views.index,name="Index"),
    path("signup/",views.signup,name="Signup"),
    path("login/",views.Login,name="Login"),
    path("logout/",views.Logout,name="Logout"),
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
    path("delete-transaction/<str:transaction_id>/",views.DeleteTransaction,name="DeleteTransaction"),
    path("transactions-filter/<str:filter>/",views.TransactionsFilter,name="TransactionFilter"),
    path("suggestions/",views.user_suggestions,name="UserSuggestions"),
    path("admin-suggestions/",views.admin_suggestions,name="AdminSuggestions"),
    path("api/suggestions/",views.SuggestionsAPI,name="SuggestionsAPI"),
    path("like/<str:suggestion_id>/",views.like,name="like"),
    path("upvote/<str:suggestion_id>/",views.upvote,name="upvote"),
    path("downvote/<str:suggestion_id>/",views.downvote,name="downvote"),
    path("api/activities/",views.ActivitiesApi,name="ActivitiesAPI"),
    path("api/users/",views.UsersApi,name="UsersAPI"),
    path("api/threads/",views.ThreadsApi,name="ThreadsAPI"),
    path("api/chat/",views.chatApi,name="ChatApi"),
    path("send-message/",views.SendMessage,name="SendMessage"),
    path("api/chat-admin/<str:username>/",views.ChatApiAdmin,name='ChatAPIAdmin'),
    path("add-suggestion/",views.suggestion,name="AddSuggestion"),
    path("add-collections/",views.AddCollections,name='AddCollection')
    
]