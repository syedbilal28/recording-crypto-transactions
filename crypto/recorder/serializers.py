from rest_framework import serializers
from .models import Transaction,Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"
class TransactionSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    class Meta:
        model=Transaction
        fields='__all__'

