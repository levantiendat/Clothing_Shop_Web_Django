from django.urls import path
from . import views

urlpatterns = [
    path('category_list/', views.category_list, name='category_list'),
    path('product_list/', views.product_list, name='product_list'),
    path('cart_list/', views.cart_list, name='cart_list'),
    path('cart_update/', views.cart_update, name='cart_update'),
    path('add_cart/', views.add_cart, name='add_cart'),
    path('update_cart_product/', views.update_cart_product, name='update_cart_product'),
    path('checkout_cart/', views.checkout_cart, name='checkout_cart'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_product/', views.add_product, name='add_product'),
    path('product_list_category/<int:category_id>/', views.product_list_category, name='product_list_category'),
    path('history_list/', views.history_list, name='history_list'),
]