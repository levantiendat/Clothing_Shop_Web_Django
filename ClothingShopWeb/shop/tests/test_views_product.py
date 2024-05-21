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
        self.login_url = reverse('login')
        self.product_list_url = reverse('product_list')
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
        # Tạo user và account tương ứng
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)
        
        self.client = Client()
        self.login_url = reverse('login')

        # Tạo thêm một số Category
        self.category1 = Category.objects.create(name='Category One')
        self.category2 = Category.objects.create(name='Category Two')

        # Tạo sản phẩm cho các Category
        self.product1 = Product.objects.create(name='Product One', price=10000, stock_number=20, category=self.category1)
        self.product2 = Product.objects.create(name='Product Two', price=20000, stock_number=30, category=self.category1)
        self.product3 = Product.objects.create(name='Product Three', price=30000, stock_number=40, category=self.category2)        
        
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
            
class AddProductViewTest(TestCase):

    def setUp(self):
        # Tạo user và account tương ứng
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)
        
        # Đăng nhập
        self.client = Client()
        self.login_url = reverse('login')
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })

        # Tạo một Category
        self.category = Category.objects.create(name='Test Category', decription='Test Description')

        self.add_product_url = reverse('add_product')
    
    def test_add_product_not_authenticated(self):
        # Kiểm tra khi user chưa đăng nhập
        self.client.logout()

        response = self.client.get(self.add_product_url)

        # Kiểm tra có chuyển hướng đến trang đăng nhập không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_add_product_view_get_authenticated(self):
        
        response = self.client.get(self.add_product_url)
        
        # Kiểm tra xem view trả về đúng template và context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_product.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.account)

    def test_add_product_authenticated_success(self):
        data = {
            'category_id': self.category.id,
            'product_name': 'Test Product',
            'product_price': 100000,
            'stock_number': 50
        }

        response = self.client.post(self.add_product_url, data)

        # Kiểm tra xem có chuyển hướng đến trang danh sách sản phẩm không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('product_list'))

        # Kiểm tra xem sản phẩm đã được tạo chưa
        self.assertTrue(Product.objects.filter(name='Test Product').exists())
        
    def test_add_product_authenticated_fail_empty_name(self):
        data = {
            'category_id': self.category.id,
            'product_name': '',
            'product_price': 100000,
            'stock_number': 50
        }

        response = self.client.post(self.add_product_url, data)


        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_product.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.account)
        self.assertIn('categories', response.context)
        # Kiểm tra danh sách các danh mục dựa trên ID
        expected_categories = [self.category]
        actual_categories = list(response.context['categories'])
        self.assertCountEqual(
            [category.pk for category in actual_categories],
            [category.pk for category in expected_categories]
        )
        
        # Kiểm tra thông báo lỗi
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Cập nhật thất bại!')

        # kiểm tra xem sản phẩm đã được tạo chưa
        self.assertFalse(Product.objects.filter(price=100.0).exists())
        
    def test_add_product_authenticated_fail_negative_stock(self):
        data = {
            'category_id': self.category.id,
            'product_name': 'Test Product',
            'product_price': 100000,
            'stock_number': -50
        }

        response = self.client.post(self.add_product_url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_product.html')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_product.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.account)
        self.assertIn('categories', response.context)
        # Kiểm tra danh sách các danh mục dựa trên ID
        expected_categories = [self.category]
        actual_categories = list(response.context['categories'])
        self.assertCountEqual(
            [category.pk for category in actual_categories],
            [category.pk for category in expected_categories]
        )

        # Kiểm tra thông báo lỗi
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Cập nhật thất bại!')

        # Kiểm tra sản phẩm không được tạo
        self.assertFalse(Product.objects.filter(price=100.0).exists())
        
    def test_add_product_authenticated_fail_negative_price(self):
        data = {
            'category_id': self.category.id,
            'product_name': 'Test Product',
            'product_price': -100000,
            'stock_number': 50
        }

        response = self.client.post(self.add_product_url, data)

        # Kiểm tra có đúng template và context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_product.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.account)
        self.assertIn('categories', response.context)
        # Kiểm tra danh sách các danh mục dựa trên ID
        expected_categories = [self.category]
        actual_categories = list(response.context['categories'])
        self.assertCountEqual(
            [category.pk for category in actual_categories],
            [category.pk for category in expected_categories]
        )

        # Kiểm tra thông báo lỗi
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Cập nhật thất bại!')

        # Kiểm tra sản phẩm không được tạo
        self.assertFalse(Product.objects.filter(price=100.0).exists())
 
class ProductUpdateViewTest(TestCase):
    def setUp(self):
        # Tạo user và account tương ứng
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)
        
        # Đăng nhập
        self.client = Client()
        self.login_url = reverse('login')
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })

        # Tạo một Category
        self.category = Category.objects.create(name='Test Category', decription='Test Description')
        # Tạo một Product
        self.product = Product.objects.create(name='Test Product', price=100000, stock_number=50, category=self.category)

        self.add_product_url = reverse('product_update', args=[self.product.id])
    
    def test_add_product_not_authenticated(self):
        # Kiểm tra khi user chưa đăng nhập
        self.client.logout()

        response = self.client.get(self.add_product_url)

        # Kiểm tra có chuyển hướng đến trang đăng nhập không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        
    def test_product_update_view_get_authenticated(self):
            
        response = self.client.get(self.add_product_url)
        
        # Kiểm tra xem view trả về đúng template và context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_update.html')
        self.assertIn('user', response.context)
        self.assertIn('product', response.context)
        self.assertIn('categories', response.context)
        self.assertEqual(response.context['user'], self.account)
        self.assertEqual(response.context['product'], self.product)
        self.assertEqual(response.context['categories'][0], self.category)

class ProductUpdateAcceptViewTest(TestCase):
    def setUp(self):
        # Tạo user và account tương ứng
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)
        
        # Đăng nhập
        self.client = Client()
        self.login_url = reverse('login')
        
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })
        
        # Tạo các Category
        self.category = Category.objects.create(name='Test Category')
        self.category2 = Category.objects.create(name='Test Category 2')
        self.category3 = Category.objects.create(name='Test Category 3')
        
        # Tạo một Product
        self.product = Product.objects.create(name='Test Product', category=self.category, price=100, stock_number=10)
        
        self.product_update_url = reverse('product_update_accept')
        
    def test_product_update_redirects_if_not_logged_in(self):
        # Kiểm tra user chưa login
        self.client.logout()
        
        data = {
            'product_id': self.product.id,
            'category_id': self.category.id,
            'product_name': 'Updated Product',
            'product_price': 150,
            'stock_number': 20,
        }
        response = self.client.post(self.product_update_url, data)
        
        # Kiểm tra có chuyển hướng đến trang đăng nhập không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_product_update_success(self):

        data = {
            'product_id': self.product.id,
            'category_id': self.category.id,
            'product_name': 'Updated Product',
            'product_price': 150,
            'stock_number': 20,
        }
        response = self.client.post(self.product_update_url, data)
        
        # Kiểm tra có chuyển hướng đến trang danh sách sản phẩm không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('product_list'))
        
        # Kiêm tra sản phẩm đã được cập nhật chưa
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')
        self.assertEqual(self.product.price, 150)
        self.assertEqual(self.product.stock_number, 20)

    def test_product_update_empty_name(self):
        data = {
            'product_id': self.product.id,
            'category_id': self.category.id,
            'product_name': '',
            'product_price': 150,
            'stock_number': 20,
        }
        response = self.client.post(self.product_update_url, data)
        
        # Kiểm tra template và context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_update.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.account)
        self.assertIn('categories', response.context)
        # Kiểm tra danh sách các danh mục dựa trên ID
        expected_categories = [self.category, self.category2, self.category3]
        actual_categories = list(response.context['categories'])
        self.assertCountEqual(
            [category.pk for category in actual_categories],
            [category.pk for category in expected_categories]
        )
        self.assertIn('product', response.context)
        self.assertEqual(response.context['product'], self.product)
        
        # Kiểm tra thông báo
        self.assertIn('messages', response.context)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Cập nhật thất bại!')
        
        # Kiểm tra sản phẩm không được cập nhật
        self.product.refresh_from_db()
        self.assertNotEqual(self.product.name, '')

    def test_product_update_negative_price(self):

        data = {
            'product_id': self.product.id,
            'category_id': self.category.id,
            'product_name': 'Updated Product',
            'product_price': -150,
            'stock_number': 20,
        }
        response = self.client.post(self.product_update_url, data)
        
        # Kiểm tra template và context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_update.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.account)
        self.assertIn('categories', response.context)
        # Kiểm tra danh sách các danh mục dựa trên ID
        expected_categories = [self.category, self.category2, self.category3]
        actual_categories = list(response.context['categories'])
        self.assertCountEqual(
            [category.pk for category in actual_categories],
            [category.pk for category in expected_categories]
        )
        self.assertIn('product', response.context)
        self.assertEqual(response.context['product'], self.product)
        
        # Kiểm tra thông báo
        self.assertIn('messages', response.context)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Cập nhật thất bại!')
        
        # Kiểm tra sản phẩm không được cập nhật
        self.product.refresh_from_db()
        self.assertNotEqual(self.product.price, -150)

    def test_product_update_negative_stock(self):

        data = {
            'product_id': self.product.id,
            'category_id': self.category.id,
            'product_name': 'Updated Product',
            'product_price': 150,
            'stock_number': -20,
        }
        response = self.client.post(self.product_update_url, data)

        # Kiểm tra template và context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_update.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.account)
        self.assertIn('categories', response.context)
        # Kiểm tra danh sách các danh mục dựa trên ID
        expected_categories = [self.category, self.category2, self.category3]
        actual_categories = list(response.context['categories'])
        self.assertCountEqual(
            [category.pk for category in actual_categories],
            [category.pk for category in expected_categories]
        )
        self.assertIn('product', response.context)
        self.assertEqual(response.context['product'], self.product)
        
        # Kiểm tra thông báo
        self.assertIn('messages', response.context)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Cập nhật thất bại!')
        
        # Kiểm tra sản phẩm không được cập nhật
        self.product.refresh_from_db()
        self.assertNotEqual(self.product.stock_number, -20)

class ProductDeleteTestCase(TestCase):
    # Tạo user và account tương ứng
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)
        
        # Đăng nhập
        self.client = Client()
        self.login_url = reverse('login')
        
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })
        
        # Tạo một Category
        self.category = Category.objects.create(name='Test Category')
        
        # Tạo một Product
        self.product = Product.objects.create(name='Test Product', category=self.category, price=100, stock_number=10)
        
        # Tạo Cart chứa Product
        self.cart = Cart.objects.create(user=self.user, product=self.product, count=1)
        
        self.product_delete_url = reverse('product_delete', args=[self.product.id])
        
    def test_product_delete_redirects_not_authenticated(self):
        # Kiểm tra user chưa login
        self.client.logout()
        
        response = self.client.get(self.product_delete_url)
        
        # Kiểm tra có chuyển hướng đến trang đăng nhập không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
                
    def test_product_delete_successful(self):
        
        response = self.client.get(self.product_delete_url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('product_list'))
        
        # Kiểm tra sản phẩm đã bị xóa
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
        self.assertFalse(Cart.objects.filter(id=self.cart.id).exists())
 
# py manage.py test shop
