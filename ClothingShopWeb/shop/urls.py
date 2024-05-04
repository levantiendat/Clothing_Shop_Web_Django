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
    path('category_update/<int:category_id>/', views.category_update, name='category_update'),
    path('category_update_accept/', views.category_update_accept, name='category_update_accept'),
    path('category_delete/<int:category_id>/', views.category_delete, name='category_delete'),
    path('product_update/<int:product_id>/', views.product_update, name='product_update'),
    path('product_update_accept/', views.product_update_accept, name='product_update_accept'),
    path('product_delete/<int:product_id>/', views.product_delete, name='product_delete'),
]