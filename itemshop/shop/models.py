from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    street = models.TextField(blank=True, null=True)
    building_address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    postal_code = models.TextField(blank=True, null=True)


class Item(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    image = models.URLField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)

class Cart(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')

    @property
    def total_price(self):
        """
        Oblicz całkowitą cenę koszyka na podstawie pozycji.
        """
        return sum(item.total_price for item in self.cart_items.all())
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        """
        Oblicz całkowity koszt tej pozycji w koszyku.
        """
        return self.quantity * self.item.price

class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)

class Order(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Utworzone'),
        ('PROCESSING', 'Procesowane'),
        ('CANCELED', 'Anulowane'),
        ('COMPLETED', 'Zakończone')
        ]
    paid = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CREATED')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
