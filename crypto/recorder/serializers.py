
from rest_framework import serializers
from .models import Transaction,Product,Suggestion,Like,Upvote,Downvote
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"

class TransactionSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    class Meta:
        model=Transaction
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"
class LikeSerializer(serializers.ModelSerializer):
    by=UserSerializer()
    class Meta:
        model=Like
        fields="__all__"

class UpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Upvote
        fields="__all__"

class DownvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Downvote
        fields="__all__"

class SuggestionSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    likes=LikeSerializer(many=True)
    upvotes=UpvoteSerializer(many=True)
    downvotes=DownvoteSerializer(many=True)
    class Meta:
        model=Suggestion
        fields=["id","user","content","timestamp","likes","upvotes","downvotes"]
