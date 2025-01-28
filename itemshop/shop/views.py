from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ItemSerializer, AddToCartSerializer, CartSerializer, OrderSerializer, CartItemSerializer

from .models import Item, Category, Cart, CartItem, OrderItem, Order


def add_to_cart(user, item_id, quantity):
    # Pobieranie koszyka użytkownika lub stwórz nowy - jwsli go nie ma
    cart, created = Cart.objects.get_or_create(user=user)
    item = Item.objects.get(id=item_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

    if not created:
        # Jeśli już istnieje, zwiększ ilość
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    return cart_item

class ItemViewSet(ModelViewSet):
    # Zwracanie listy itemów, pojdeynczego itemu, dodawanie itemu, usuwanie itemu
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    @action(methods=['POST'], detail=False)
    def add(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            item_id = serializer.validated_data['item_id']
            quantity = serializer.validated_data['quantity']
            print("USER", request.user, quantity, item_id)
            # Dodanie do koszyka
            cart_item = add_to_cart(request.user, item_id, quantity)
            return Response(
                {"message": "Pzredmio dodany do koszyka.",},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrderViewSet(ModelViewSet):
    #  CRUD do zamówienia

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Pobieram koszyk uzytkownika
        user_cart = self.request.user.cards.first()
        # a teraz wszystkie itemy z koszyka
        cart_items = user_cart.cart_items.all()
        total_price = sum(item.quantity * item.item.price for item in cart_items)


        # Tworzenie zamówienia
        order = serializer.save(user=self.request.user, total_price=total_price)
        # Przeniesienie produktów z koszyka do zamówienia
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                item=cart_item.item,
                quantity=cart_item.quantity,
            )

        # Czyszczenie koszyka po utworzeniu zamówienia
        user_cart.delete()
    serializer_class = OrderSerializer