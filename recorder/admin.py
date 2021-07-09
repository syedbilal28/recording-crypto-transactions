from django.contrib import admin
from .models import Collection,Type,Product,Transaction,GasFee,Inventory,Suggestion,Like,Upvote,Downvote
# Register your models here.
admin.site.register(Collection)
admin.site.register(Type)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(GasFee)
admin.site.register(Inventory)
admin.site.register(Suggestion)
admin.site.register(Like)
admin.site.register(Upvote)
admin.site.register(Downvote)