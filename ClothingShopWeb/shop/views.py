from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Category, Product, Cart
from accounts.models import Account
import locale

def category_list(request):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    if user.role is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories, 'user': user})

def product_list(request):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    if user.role is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    products = Product.objects.all()
    for product in products:
        product.price = "{:,.0f}".format(product.price)
    return render(request, 'product_list.html', {'products': products, 'user': user})

def add_cart(request):
    username = request.session.get("user", None)
    user = Account.objects.get(user__username=username)
    user1 = user.user
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_id = int(product_id)
        
        if product_id:
            product = Product.objects.get(pk=product_id)
            try:
                cart_item = Cart.objects.get(user=user1, product=product)
                cart_item.count += 1
                cart_item.save()
                messages.success(request, f'Đã tăng số lượng thành {0} vào giỏ hàng!'.format(cart_item.count))
            except Cart.DoesNotExist:
                cart_item = Cart.objects.create(user=user1, product=product, count = 1)
                messages.success(request, 'Sản phẩm đã được thêm vào giỏ hàng!')
    return redirect('product_list')

def cart_list(request):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    user1 = user.user
    if user.role is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    carts = Cart.objects.filter(user=user1)  # Lọc các đối tượng Cart theo username của người dùng
    return render(request, 'cart_list.html', {'carts': carts, 'user': user})

def cart_update(request):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    if user.role is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    cart_id = '1'  # Lấy id của Cart hiện tại
    cart = Cart.objects.filter(id=cart_id)  # Lọc các đối tượng Cart theo id của Cart
    return render(request, 'cart_update.html', {'cart': cart, 'user': user})