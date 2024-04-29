from django.shortcuts import render, redirect
from .models import Category, Product

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