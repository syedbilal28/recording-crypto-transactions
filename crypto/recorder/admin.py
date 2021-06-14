from django.contrib import admin
from .models import Collection,Type,Product,Transaction
# Register your models here.
admin.site.register(Collection)
admin.site.register(Type)
admin.site.register(Product)
admin.site.register(Transaction)
