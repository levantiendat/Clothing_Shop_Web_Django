from django.urls import path
from . import views

urlpatterns = [
    path('category_list/', views.category_list, name='category_list'),
    path('product_list/', views.product_list, name='product_list'),
    path('cart_list/', views.cart_list, name='cart_list'),
    path('cart_update/', views.cart_update, name='cart_update'),
    path('add_cart/', views.add_cart, name='add_cart'),
]