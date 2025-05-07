from rest_framework import serializers
from .models import Product, Category,  CartItem, Order, Table
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product  # Product modeli to'g'ri import qilinganligiga ishonch hosil qiling
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'number']