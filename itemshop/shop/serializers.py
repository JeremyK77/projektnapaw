from rest_framework import serializers

from .models import User, CartItem, Cart, Item, OrderItem, Order, Category


class UserSerializer(serializers.ModelSerializer):
    # Serializowanie danych rozszerzonego modelu User - dodanie nowych pól
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'building_address', 'street', 'city', 'postal_code']

class ItemSerializer(serializers.ModelSerializer):
    # Serializowanie danych itemów (produktów) sklepu

    class Meta:
        model = Item
        fields = "__all__"

class CartItemSerializer(serializers.ModelSerializer):
    # Serializowanie danych itemów w koszyku

    item = ItemSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "item", "quantity"]

class CartSerializer(serializers.ModelSerializer):
    # Serializowanie danych koszyka

    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'cart_items']

class OrderItemSerializer(serializers.ModelSerializer):
    # Serializowanie danych itemów w zamówienia

    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    # Serializowanie danych zamówienia

    order_items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        

class CategorySerializer(serializers.ModelSerializer):
    # Serializowanie danych kategorii

    class Meta:
        model = Category
        fields = "__all__"


class AddToCartSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)