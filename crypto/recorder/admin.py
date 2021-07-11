from django.contrib import admin
from .models import Collection,Currency,Product,Transaction,GasFee,Inventory,Suggestion,Like,Upvote,Downvote,ChatMessage,Thread
# Register your models here.
admin.site.register(Collection)
admin.site.register(Currency)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(GasFee)
admin.site.register(Inventory)
admin.site.register(Suggestion)
admin.site.register(Like)
admin.site.register(Upvote)
admin.site.register(Downvote)


class ChatMessage(admin.TabularInline):
    model = ChatMessage

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread 


admin.site.register(Thread, ThreadAdmin)
