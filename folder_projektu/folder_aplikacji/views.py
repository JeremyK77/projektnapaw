# views.py
from django.shortcuts import render
from .models import Item, Cart, Order

def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})

def cart(request):
    # Pobierz koszyk użytkownika
    user_cart = Cart.objects.filter(user=request.user).first()
    return render(request, 'cart.html', {'cart': user_cart})

def order_list(request):
    # Pobierz zamówienia użytkownika
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_list.html', {'orders': orders})