
from enum import auto
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os
# Create your models here.

def to_upload(instance,filename):
    # path_to_upload=os.path(instance.username+"/ProfilePicture")
    directory= os.path.join(settings.MEDIA_ROOT,"Collection")
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    directory_profile = os.path.join(directory,instance.name)
    try:
        os.stat(directory_profile)
    except:
        os.mkdir(directory_profile)
    return f"Collection/{instance.name}/{filename}"

def to_upload_type(instance,filename):
    # path_to_upload=os.path(instance.username+"/ProfilePicture")
    directory= os.path.join(settings.MEDIA_ROOT,"type")
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    directory_profile = os.path.join(directory,instance.name)
    try:
        os.stat(directory_profile)
    except:
        os.mkdir(directory_profile)
    return f"type/{instance.name}/{filename}"

def upload_product(instance,filename):
    # path_to_upload=os.path(instance.username+"/ProfilePicture")
    directory= os.path.join(settings.MEDIA_ROOT,"Products")
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    directory_profile = os.path.join(directory,instance.name)
    try:
        os.stat(directory_profile)
    except:
        os.mkdir(directory_profile)
    return f"Products/{instance.name}/{filename}"



class Suggestion(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content= models.CharField(max_length=1000)
    timestamp=models.DateTimeField(auto_now_add=True)

    def like(self,user):
        try:
            like=Like.objects.get(by=user,suggestion=self)
            self.dislike(like)
            return False
        except:

            Like.objects.create(by=user,suggestion=self)
            return True
    def dislike(self,like_object):
        like_object.delete()
        return True
    def upvote(self,user):
        try:
            vote=Downvote.objects.get(by=user,suggestion=self)
        except:
            vote= None
        if vote:
            vote.delete()
        try:
            Upvote.objects.create(by=user,suggestion=self)
        except:
            return False
        return True
    def downvote(self,user):
        try:
            vote=Upvote.objects.get(by=user,suggestion=self)
        except:
            vote= None
        if vote:
            vote.delete()
        try:
            Downvote.objects.create(by=user,suggestion=self)
        except:
            return False
        return True
class Like(models.Model):
    by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="likes") 
    suggestion = models.ForeignKey(Suggestion,on_delete=models.CASCADE,related_name="likes")

    class Meta:
        unique_together=("by","suggestion")
    def __str__(self):
        return f"{self.suggestion.user.username}: {self.by.username} {self.suggestion.pk}"
class Upvote(models.Model):
    by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="upvotes") 
    suggestion = models.ForeignKey(Suggestion,on_delete=models.CASCADE,related_name="upvotes")
    class Meta:
        unique_together=("by","suggestion")
    def __str__(self):
        return f"{self.suggestion.user.username}: {self.by.username} {self.suggestion.pk}"

class Downvote(models.Model):
    by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="downvotes") 
    suggestion = models.ForeignKey(Suggestion,on_delete=models.CASCADE,related_name="downvotes")
    class Meta:
        unique_together=("by","suggestion")
    def __str__(self):
        return f"{self.suggestion.user.username}: {self.by.username} {self.suggestion.pk}"

class Collection(models.Model):
    name=models.CharField(max_length=100)
    logo=models.ImageField(upload_to=to_upload)

    def __str__(self):
        return self.name

# class Type(models.Model):
#     name=models.CharField(max_length=100)
#     logo=models.ImageField(upload_to=to_upload_type)
#     def __str__(self):
#         return self.name
    
    
class Product(models.Model):
    name=models.CharField(max_length=100)
    collection=models.ForeignKey(Collection,on_delete=models.CASCADE)
    # Type=models.ForeignKey("Type",on_delete=models.CASCADE)
    image= models.ImageField(upload_to=upload_product)
    def __str__(self):
        return self.name

class Transaction(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.FloatField()
    Type= models.CharField(max_length=10)
    quantity=models.IntegerField()
    percentage=models.FloatField(null=True,blank=True)
    timestamp=models.DateField(null=True)
    note= models.CharField(max_length=2000,null=True)
    profit= models.FloatField(default=0,blank=True)
    cost_per_piece=models.FloatField(default=0,null=True,blank=True)
    def __str__(self):
        return f"{self.pk}: {self.Type}"
class Currency(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class GasFee(models.Model):
    currency=models.ForeignKey(Currency,null=True,on_delete=models.SET_NULL)
    date=models.DateField()
    fee=models.FloatField()

class Inventory(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    available_quantity=models.IntegerField(default=0)
class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = models.Q(first=user) | models.Q(second=user)
        qlookup2 = models.Q(first=user) & models.Q(second=user)
        qs =  qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, other_username):  # get_or_create
        first_user = user
        if first_user.username == other_username:
            return None
        other_user=User.objects.get(username=other_username)
        qlookup1 = models.Q(first=first_user) & models.Q(second=other_user)
        qlookup2 = models.Q(first=other_user) & models.Q(second=first_user)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = first_user.__class__
            user2 = other_user
            if user != user2:
                obj = self.model(
                    first=first_user,
                    second=user2
                )
                obj.save()
                return obj, True
            return None, False
    

class Thread(models.Model):
    first = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_thread_first')
    second = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_thread_second')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        ordering=('-updated',)
    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
            return True
        return False


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL,related_name="chat")
    user = models.ForeignKey(User, verbose_name='sender', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        ordering=('timestamp',)


class EmailMessage(models.Model):
    name=models.CharField(max_length=200)
    email= models.EmailField(max_length=100)
    message=models.CharField(max_length=1500)


    