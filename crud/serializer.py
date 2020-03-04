from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.hashers import make_password


class Product2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product2
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class ProductoCarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoCarrito
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class StatusPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusCarrito
        fields = '__all__'

