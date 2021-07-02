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



class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content= models.CharField(max_length=1000)
    timestamp=models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="like") 
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

class Upvote(models.Model):
    by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="upvote") 
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

class Downvote(models.Model):
    by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="downvote") 
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

class Collection(models.Model):
    name=models.CharField(max_length=100)
    logo=models.ImageField(upload_to=to_upload)

    def __str__(self):
        return self.name

class Type(models.Model):
    name=models.CharField(max_length=100)
    logo=models.ImageField(upload_to=to_upload_type)
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name=models.CharField(max_length=100)
    collection=models.ForeignKey(Collection,on_delete=models.CASCADE)
    Type=models.ForeignKey("Type",on_delete=models.CASCADE)
    image= models.ImageField(upload_to=upload_product)
    def __str__(self):
        return self.name

class Transaction(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.IntegerField()
    Type= models.CharField(max_length=10)
    quantity=models.IntegerField()
    percentage=models.FloatField(null=True,blank=True)
    timestamp=models.DateField(null=True)
    note= models.CharField(max_length=2000,null=True)
    profit= models.FloatField(null=True,blank=True)

class GasFee(models.Model):
    currency=models.CharField(max_length=100,null=True,blank=True)
    date=models.DateField()
    fee=models.FloatField()

class Inventory(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    available_quantity=models.IntegerField(default=0)




    