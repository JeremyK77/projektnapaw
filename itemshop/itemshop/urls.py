
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from shop.views import ItemViewSet, CartViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'item', ItemViewSet, basename='item')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    # Muszę to dodać, żeby można było używać CRUD item, category itd...
    path('', include(router.urls)),

    # Ten endpoint służy do generowanie tokena do logowwania
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    path('admin/', admin.site.urls),
]

