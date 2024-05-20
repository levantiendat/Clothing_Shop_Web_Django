from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Account
from shop.models import Category, Product, History, Cart
from django.utils import timezone
import json

class ProductListViewTest(TestCase):
    def setUp(self):
        # Tạo user và account tương ứng
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.login_url = reverse('login')  # Thay thế 'login' bằng tên đường dẫn của trang đăng nhập của bạn
        self.product_list_url = reverse('product_list')  # Thay thế 'product_list' bằng tên đường dẫn của view product_list
        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)
        
        # Tạo thêm một số Category
        category1 = Category.objects.create(name='Category One', decription='Description One')
        category2 = Category.objects.create(name='Category Two', decription='Description Two')
        
        # Tạo thêm một số Product
        self.product1 = Product.objects.create(name='Product One', price=10000, stock_number=10, category=category1)
        self.product2 = Product.objects.create(name='Product Two', price=20000, stock_number=20, category=category2)
        
        # Đăng nhập
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })

    def test_product_list_view_not_authenticated(self):
        # Test khi user chưa đăng nhập
        self.client.logout()
        
        response = self.client.get(self.product_list_url)
        
        # Kiểm tra xem có chuyển hướng đến trang đăng nhập không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_product_list_view_authenticated(self):
        
        response = self.client.get(self.product_list_url)
        
        # Kiểm tra xem view trả về đúng template và context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_list.html')
        
        # Kiểm tra context có chứa đúng thông tin của người dùng hiện tại và danh sách tất cả các sản phẩm
        self.assertIn('user', response.context)
        self.assertIn('products', response.context)
        self.assertEqual(response.context['user'], self.account)

        # Kiểm tra danh sách các sản phẩm dựa trên ID và giá định dạng
        actual_products = [self.product1, self.product2]
        expected_products = list(response.context['products'])
        self.assertCountEqual(
            [product.pk for product in actual_products],
            [product.pk for product in expected_products]
        )

        # Kiểm tra giá sản phẩm được định dạng đúng
        for i, product in enumerate(actual_products):
            formatted_price = "{:,.0f}".format(int(product.price))
            self.assertEqual(expected_products[i].price, formatted_price)

class ProductListCategoryViewTest(TestCase):
    def setUp(self):
        # Create a user and corresponding account
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.login_url = reverse('login')  # Replace 'login' with the actual name of your login URL

        # Create categories
        self.category1 = Category.objects.create(name='Category One')
        self.category2 = Category.objects.create(name='Category Two')

        # Create products in each category
        self.product1 = Product.objects.create(name='Product One', price=10000, stock_number=20, category=self.category1)
        self.product2 = Product.objects.create(name='Product Two', price=20000, stock_number=30, category=self.category1)
        self.product3 = Product.objects.create(name='Product Three', price=30000, stock_number=40, category=self.category2)

        # Create account for the user
        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)
        
        self.product_list_category_url = reverse('product_list_category', args=[self.category1.id])
        
        # Đăng nhập
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })


    def test_product_list_category_view_not_authenticated(self):
        # Test khi user chưa đăng nhập
        self.client.logout()
        
        response = self.client.get(self.product_list_category_url)
        
        # Kiểm tra xem có chuyển hướng đến trang đăng nhập không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_product_list_category_view_authenticated(self):
        
        response = self.client.get(self.product_list_category_url)
        
        # Kiểm tra xem view trả về đúng template và context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_list.html')
        
        # Kiểm tra context có chứa đúng thông tin của người dùng hiện tại và danh sách tất cả các sản phẩm
        self.assertIn('user', response.context)
        self.assertIn('products', response.context)
        self.assertEqual(response.context['user'], self.account)

        # Kiểm tra danh sách các sản phẩm dựa trên ID và giá định dạng
        actual_products = [self.product1, self.product2]
        expected_products = list(response.context['products'])
        self.assertCountEqual(
            [product.pk for product in actual_products],
            [product.pk for product in expected_products]
        )

        # Kiểm tra giá sản phẩm được định dạng đúng
        for i, product in enumerate(actual_products):
            formatted_price = "{:,.0f}".format(int(product.price))
            self.assertEqual(expected_products[i].price, formatted_price)
            
            
# py manage.py test shop