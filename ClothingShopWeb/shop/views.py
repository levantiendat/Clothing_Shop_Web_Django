from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Category, Product, Cart, History
from accounts.models import Account
import locale
from django.utils import timezone
import pytz

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

def product_list_category(request, category_id):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    if user.role is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    category = Category.objects.get(id = category_id)
    products = Product.objects.filter(category = category)
    for product in products:
        product.price = "{:,.0f}".format(product.price)
    return render(request, 'product_list.html', {'products': products, 'user': user})

def add_category(request):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    user1 = user.user
    if user.role is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    if request.method == 'POST':
        name = request.POST.get('category_name')
        decription = request.POST.get('decription')
        try:
            category = Category.objects.create(name=name, decription=decription)
            return redirect('category_list')
        except:
            messages.error(request, 'Thêm thất bại!')
            return render(request, 'add_category.html', {'user': user})
    else:
        return render(request, 'add_category.html', {'user': user})
    
def category_update(request, category_id):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    if user.role is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    
    category = Category.objects.get(id = category_id)
    return render(request, 'category_update.html', {'user': user, 'category': category})
def category_update_accept(request):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    if user.role is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        name = request.POST.get('category_name')
        decription = request.POST.get('decription')
        try:
            category = Category.objects.get(id = category_id)
            category.name = name
            category.decription = decription
            category.save()
            return redirect('category_list')
        except Exception as e:
            print(e)
            messages.error(request, 'Thêm thất bại!')
            category = Category.objects.get(id = category_id)
            return render(request, 'category_update.html', {'user': user, 'category': category})

def category_delete(request, category_id):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    if user.role is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    category = Category.objects.get(id = category_id)
    products = Product.objects.filter(category = category)
    for product in products:
        carts = Cart.objects.filter(product = product)
        carts.delete()
    products.delete()
    category.delete()
    return redirect('category_list')
def add_product(request):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    user1 = user.user
    categories = Category.objects.all()
    if user.role is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    if request.method == 'POST':
        try:
            category_id = request.POST.get('category_id')
            
            name = request.POST.get('product_name')
            price = request.POST.get('product_price')
            stock_number = request.POST.get('stock_number')
            category_id = int(category_id)
            category = Category.objects.get(id = category_id)
            product = Product.objects.create(name=name, category=category, price=price, stock_number=stock_number)
        
            return redirect('product_list')
        except Exception as e:
            print(e)
            messages.error(request, 'Cập nhật thất bại!')
            return render(request, 'add_product.html', {'user': user, 'categories': categories})
    else:
        return render(request, 'add_product.html', {'user': user, 'categories': categories})

def product_update(request, product_id):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    if user.role is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    categories = Category.objects.all()
    product = Product.objects.get(id = product_id)
    return render(request, 'product_update.html', {'user': user,'categories':categories, 'product': product})
def product_update_accept(request):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    if user.role is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        category_id = request.POST.get('category_id')
        name = request.POST.get('product_name')
        price = request.POST.get('product_price')
        stock_number = request.POST.get('stock_number')
        category_id = int(category_id)
        category = Category.objects.get(id = category_id)
        
        try:
            product = Product.objects.get(id = product_id)
            product.category = category
            product.name = name
            product.price = price
            product.stock_number = stock_number
            product.save()
            return redirect('product_list')
        except Exception as e:
            print(e)
            messages.error(request, 'Cập nhật thất bại!')
            categories = Category.objects.all()
            product = Product.objects.get(id = product_id)
            return render(request, 'product_update.html', {'user': user,'categories':categories, 'product': product})

def product_delete(request, product_id):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    if user.role is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    product =  Product.objects.get(id = product_id)
    carts = Cart.objects.filter(product = product)
    carts.delete()
    product.delete()
    return redirect('product_list')

def add_cart(request):
    username = request.session.get("user", None)
    user = Account.objects.get(user__username=username)
    user1 = user.user
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_id = int(product_id)
        
        if product_id:
            product = Product.objects.get(pk=product_id)
            cart_counts = Cart.objects.filter(product=product)
            count = 0
            for cart_count in cart_counts:
                count+=cart_count.count
            if count < product.stock_number:

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
    total_cart = 0
    for cart in carts:
        total_cart +=cart.count*cart.product.price
    return render(request, 'cart_list.html', {'carts': carts, 'user': user, 'total_cart': total_cart})

def cart_update(request):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    if user.role is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    cart_id = request.POST.get('cart_id')  # Lấy id của Cart hiện tại
    cart_id = int(cart_id)
    cart = Cart.objects.filter(id=cart_id)  # Lọc các đối tượng Cart theo id của Cart
    cart = cart[0]
    product_id = int(cart.product.id)
    product = Product.objects.get(pk=product_id)  # Lấy thông tin sản phẩm từ Cart
    return render(request, 'cart_update.html', {'cart': cart, 'product': product, 'user': user})

def update_cart_product(request):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        cart_id = int(cart_id)
        cart_new_count = request.POST.get('cart_new_count')
        cart_new_count = int(cart_new_count)
        
        if(cart_new_count < 0):
            messages.error(request, 'Số lượng sản phẩm phải lớn hơn 0!')
        elif(cart_new_count == 0):
            Cart.objects.filter(pk = cart_id).delete()
        else:
            cart = Cart.objects.get(pk=cart_id)
        
            try:
                cart.count = int(cart_new_count)
                cart.save()
                messages.success(request, 'Đã cập nhật số lượng sản phẩm trong giỏ hàng!')
            except Exception as e:
                messages.error(request, e)
    
    return redirect('cart_list')

def delete_cart_product(request):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    
    cart_id = request.POST.get('cart_id')
    cart = Cart.objects.get(pk=cart_id)
    
    try:
        cart.delete()
        messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng!')
    except Exception as e:
        messages.error(request, e)
        
    return redirect('cart_list')

def checkout_cart(request):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    user1 = user.user

    if user.role is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    carts = Cart.objects.filter(user=user1)  # Lọc các đối tượng Cart theo username của người dùng
    total_cart = 0
    for cart in carts:
        total_cart +=cart.count*cart.product.price
    current_time_vn = timezone.localtime(timezone.now(), pytz.timezone('Asia/Ho_Chi_Minh'))

    try:
        history = History.objects.create(user=user1, date=current_time_vn, total_amount=total_cart)
        carts = Cart.objects.filter(user=user1)
        for cart in carts:
            product = cart.product
            product.stock_number -= cart.count
            product.save()
        Cart.objects.filter(user=user1).delete()
        messages.success(request, 'Hóa đơn đã được thanh toán!')
    except Exception as e:
        print(e)
        messages.error(request, 'Thanh toán thất bại!')
    return redirect('cart_list')

def history_list(request):
    username = request.session.get("user", None)  # Lấy thông tin của người dùng từ session
    user = Account.objects.get(user__username=username)
    user1 = user.user
    if user.role is None:
        return redirect("login")  # Chuyển hướng đến trang đăng nhập nếu không có quyền truy cập
    if user.role == 1:
        histories = History.objects.all()
        
    else:
        histories = History.objects.filter(user = user1)
    for history in histories:
        history.total_amount = "{:,.0f}".format(history.total_amount)
    return render(request, 'history_list.html', {'histories': histories, 'user': user})
