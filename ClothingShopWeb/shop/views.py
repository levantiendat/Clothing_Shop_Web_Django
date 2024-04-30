from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Category, Product, Cart

def category_list(request):
    roles = request.session.get("role", None)  # Lấy quyền của người dùng từ session
    if roles is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories, 'roles': roles})

def product_list(request):
    roles = request.session.get("role", None)  # Lấy quyền của người dùng từ session
    if roles is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products, 'roles': roles})

def cart_list(request):
    roles = request.session.get("role", None)  # Lấy quyền của người dùng từ session
    # if roles is None:
    #     return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    username = request.user.username  # Lấy username của người dùng hiện tại
    cart = Cart.objects.filter(user__username=username)  # Lọc các đối tượng Cart theo username của người dùng
    return render(request, 'cart_list.html', {'cart': cart, 'roles': roles})

def cart_update(request):
    roles = request.session.get("role", None)  # Lấy quyền của người dùng từ session
    # if roles is None:
    #     return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    cart_id = '1'  # Lấy id của Cart hiện tại
    cart = Cart.objects.filter(id=cart_id)  # Lọc các đối tượng Cart theo id của Cart
    return render(request, 'cart_update.html', {'cart': cart, 'roles': roles})