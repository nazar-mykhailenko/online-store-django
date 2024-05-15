from django.urls import path
from . import views


app_name = 'cart'
urlpatterns = [
    path('cart', views.cart, name='cart'),
    path('cart-add/<int:product_id>', views.cart_add, name='cart-add'),
    path('cart-remove/<int:product_id>', views.cart_remove, name='cart-remove'),
    path('cart-remove-all/<int:product_id>', views.cart_remove_completely, name='cart-remove-all')
]
