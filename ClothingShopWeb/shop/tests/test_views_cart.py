from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Account
from shop.models import Category, Product, History, Cart
from django.utils import timezone
from django.contrib.messages import get_messages
import json

class HistoryListViewTest(TestCase):
    def setUp(self):
        # Tạo người dùng và tài khoản
        self.password = 'testpassword'
        self.user1 = User.objects.create_user(username='testuser1', password=self.password)
        self.account1 = Account.objects.create(user=self.user1, name='Test User 1', phone_number='1234567890', role=0)
        
        self.user2 = User.objects.create_user(username='testuser2', password=self.password)
        self.account2 = Account.objects.create(user=self.user2, name='Test User 2', phone_number='0987654321', role=1)
        
        # Tạo lịch sử mua hàng
        self.history1 = History.objects.create(user=self.user1, total_amount=1000, date=timezone.now())
        self.history2 = History.objects.create(user=self.user2, total_amount=2000, date=timezone.now())
        
        self.client = Client()
        self.login_url = reverse('login')
        
        self.history_list_url = reverse('history_list')

    def test_history_list_redirects_if_not_logged_in(self):
        
        response = self.client.get(self.history_list_url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_history_list_user_role_0(self):
        # Đăng nhập khách hàng
        self.client.post(self.login_url, {
            'username': 'testuser1',
            'password': self.password
        })
        response = self.client.post(self.history_list_url)
        
        # Kiểm tra chuyển qua trang lịch sử mua hàng
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'history_list.html')
        self.assertIn('user', response.context)
        self.assertIn('histories', response.context)
        self.assertEqual(response.context['user'], self.account1)
        self.assertEqual(len(response.context['histories']), 1)
        self.assertEqual(response.context['histories'][0], self.history1)
        
        # Kiểm tra chỉ hiển thị lịch sử của người dùng hiện tại
        self.assertContains(response, '1,000')
        self.assertNotContains(response, '2,000')

    def test_history_list_user_role_1(self):
        # Đăng nhập khách hàng
        self.client.post(self.login_url, {
            'username': 'testuser2',
            'password': self.password
        })
        response = self.client.post(self.history_list_url)
        
        # Kiểm tra chuyển qua trang lịch sử mua hàng
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'history_list.html')
        self.assertIn('user', response.context)
        self.assertIn('histories', response.context)
        self.assertEqual(response.context['user'], self.account2)
        self.assertEqual(len(response.context['histories']), 2)
        self.assertEqual(response.context['histories'][0], self.history1)
        self.assertEqual(response.context['histories'][1], self.history2)
        
        # Kiểm tra hiển thị tất cả lịch sử mua hàng
        self.assertContains(response, '1,000')
        self.assertContains(response, '2,000')

# py manage.py test shop.tests.test_views_cart.HistoryListViewTest
class AddCartViewTest(TestCase):
    def setUp(self):
        # Tạo user và account tương ứng
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)
        
        # Tạo sản phẩm và danh mục tương ứng
        self.category = Category.objects.create(name='Test Category', decription='A test category description')
        self.product = Product.objects.create(name='Test Product', price=100, stock_number=10, category=self.category)
        
        # Đăng nhập
        self.client = Client()
        self.login_url = reverse('login')
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })
        
        self.add_cart_url = reverse('add_cart')
    
    def test_add_cart_redirects_if_not_logged_in(self):
        # Kiểm tra user chưa đăng nhập
        self.client.logout()
        
        response = self.client.get(self.add_cart_url, {'product_id': self.product.id})
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        
    def test_add_product_to_cart_first_time(self):
        # Thêm sản phẩm vào giỏ hàng lần đầu        
        response = self.client.post(self.add_cart_url, {'product_id': self.product.id})
        
        # Kiểm tra chuyển hướng đến trang danh sách sản phẩm
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('product_list'))
        
        # Kiểm tra sản phẩm đã được thêm vào giỏ hàng
        cart_item = Cart.objects.get(user=self.user, product=self.product)
        self.assertEqual(cart_item.count, 1)
        
    def test_increase_product_quantity_in_cart(self):
        # Thêm sản phẩm đã có có trong giỏ hàng
        Cart.objects.create(user=self.user, product=self.product, count=3)
        
        response = self.client.post(self.add_cart_url, {'product_id': self.product.id})
        
        # Kiểm tra chuyển hướng đến trang danh sách sản phẩm
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('product_list'))
        
        # Kiểm tra số lượng sản phẩm đã được tăng
        cart_item = Cart.objects.get(user=self.user, product=self.product)
        self.assertEqual(cart_item.count, 4)
        
    def test_add_product_exceeding_stock_number(self):        
        # Thêm sản phẩm với số lượng vượt quá số lượng tồn kho
        # Tạo giỏ hàng với số lượng sản phẩm bằng số lượng tồn kho
        Cart.objects.create(user=self.user, product=self.product, count=self.product.stock_number)
        
        response = self.client.post(self.add_cart_url, {'product_id': self.product.id})
        
        # Kiểm tra chuyển hướng đến trang danh sách sản phẩm
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('product_list'))
        
        # Kiểm tra số lượng sản phẩm trong giỏ không thay đổi
        cart_item = Cart.objects.get(user=self.user, product=self.product)
        self.assertEqual(cart_item.count, self.product.stock_number)
        
    def test_add_product_with_no_stock(self):
        # Thêm sản phẩm với số lượng tồn kho bằng 0
                
        # Đặt số lượng tồn kho bằng 0
        self.product.stock_number = 0
        self.product.save()
        
        response = self.client.post(self.add_cart_url, {'product_id': self.product.id})
        
        # Kiểm tra chuyển hướng đến trang danh sách sản phẩm
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('product_list'))
        
        # Kiểm tra sản phẩm không được thêm vào giỏ hàng
        cart_items = Cart.objects.filter(user=self.user, product=self.product)
        self.assertEqual(cart_items.count(), 0)

# py manage.py test shop.tests.test_views_cart.AddCartViewTest
class CartListViewTest(TestCase):
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
        
        self.cart_list_url = reverse('cart_list')
        
        # Tạo sản phẩm và danh mục tương ứng
        self.category = Category.objects.create(name='Test Category', decription='A test category description')
        self.product1 = Product.objects.create(name='Test Product', price=100, stock_number=10, category=self.category)
        self.product2 = Product.objects.create(name='Test Product 2', price=200, stock_number=20, category=self.category)
        
    def test_cart_list_redirects_if_not_logged_in(self):
        # Kiểm tra user chưa đăng nhập
        self.client.logout()
        
        response = self.client.get(self.cart_list_url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        
    def test_cart_list_user_with_items(self): # đã đăng nhập và có sản phẩm trong giỏ hàng
        # Tạo giỏ hàng
        Cart.objects.create(user=self.user, product=self.product1, count=2)
        Cart.objects.create(user=self.user, product=self.product2, count=1)
        
        response = self.client.get(self.cart_list_url)
        
        # Kiểm tra chuyển hướng đến trang giỏ hàng
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart_list.html')
        self.assertIn('user', response.context)
        self.assertIn('carts', response.context)
        self.assertIn('total_cart', response.context)
        
        # Kiểm tra thông tin giỏ hàng
        self.assertEqual(response.context['user'], self.account)
        self.assertEqual(len(response.context['carts']), 2)
        self.assertEqual(response.context['carts'][0].product, self.product1)
        self.assertEqual(response.context['carts'][1].product, self.product2)
        self.assertEqual(response.context['total_cart'], 400)
    
    def test_cart_list_user_with_no_items(self): # Đã đăng nhập nhưng không có sản phẩm trong giỏ hàng
        response = self.client.get(self.cart_list_url)
        
        # Kiểm tra chuyển hướng đến trang giỏ hàng
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart_list.html')
        self.assertIn('user', response.context)
        self.assertIn('carts', response.context)
        self.assertIn('total_cart', response.context)
        
        # Kiểm tra thông tin giỏ hàng
        self.assertEqual(response.context['user'], self.account)
        self.assertEqual(len(response.context['carts']), 0)
        self.assertEqual(response.context['total_cart'], 0)

# py manage.py test shop.tests.test_views_cart.CartListViewTest
class CartUpdateViewTest(TestCase):

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
        
        # Tạo giỏ hàng, sản phẩm và danh mục tương ứng
        self.category = Category.objects.create(name='Test Category', decription='A test category description')
        self.product = Product.objects.create(name='Test Product', price=100, stock_number=10, category=self.category)
        self.cart = Cart.objects.create(user=self.user, product=self.product, count=2)
        
        self.update_cart_url = reverse('cart_update')

    def test_cart_update_not_logged_in(self):
        # Kiểm tra user chưa đăng nhập
        self.client.logout()
        
        response = self.client.post(self.update_cart_url, {'cart_id': self.cart.id})
        
        # Kiểm tra chuyển hướng đến trang đăng nhập
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_cart_update_logged_in(self):
        
        response = self.client.post(self.update_cart_url, {'cart_id': self.cart.id})
        
        # Kiểm tra trả về trang cập nhật giỏ hàng
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart_update.html')
        self.assertIn('user', response.context)
        self.assertIn('cart', response.context)
        self.assertIn('product', response.context)
        
        # Kiểm tra thông tin giỏ hàng
        self.assertEqual(response.context['user'], self.account)
        self.assertEqual(response.context['cart'], self.cart)
        self.assertEqual(response.context['product'], self.product)

# py manage.py test shop.tests.test_views_cart.CartUpdateViewTest
class UpdateCartProductViewTest(TestCase):

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
        
        # Tạo giỏ hàng, sản phẩm và danh mục tương ứng
        self.category = Category.objects.create(name='Test Category', decription='A test category description')
        self.product = Product.objects.create(name='Test Product', price=100, stock_number=10, category=self.category)
        self.cart = Cart.objects.create(user=self.user, product=self.product, count=2)
        
        self.update_cart_product_url = reverse('update_cart_product')
        self.cart_list_url = reverse('cart_list')

    def test_update_cart_product_not_logged_in(self):
        # Kiểm tra user chưa đăng nhập
        self.client.logout()
        
        response = self.client.post(self.update_cart_product_url, {
            'cart_id': self.cart.id,
            'cart_new_count': 3
        })
        
        # Kiểm tra chuyển hướng đến trang đăng nhập
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_update_cart_product_logged_in_valid_quantity(self):
        response = self.client.post(self.update_cart_product_url, {
            'cart_id': self.cart.id,
            'cart_new_count': 3
        })
        
        # Kiểm tra chuyển hướng đến trang danh sách giỏ hàng
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart_list'))
        
        # Kiểm tra thông báo
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Đã cập nhật số lượng sản phẩm trong giỏ hàng!')
        
        # Kiểm tra số lượng sản phẩm đã được cập nhật
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.count, 3)

    def test_update_cart_product_logged_in_zero_quantity(self):
        
        response = self.client.post(self.update_cart_product_url, {
            'cart_id': self.cart.id,
            'cart_new_count': 0
        })
        
        # Kiểm tra chuyển hướng đến trang danh sách giỏ hàng
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart_list'))
        
        # Kiểm tra sản phẩm không có trong giỏ hàng
        with self.assertRaises(Cart.DoesNotExist):
            Cart.objects.get(pk=self.cart.id)
        
    def test_update_cart_product_logged_in_negative_quantity(self):
        response = self.client.post(self.update_cart_product_url, {
            'cart_id': self.cart.id,
            'cart_new_count': -1
        })
        
        # Kiểm tra chuyển hướng đến trang danh sách giỏ hàng
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart_list'))
        
        # Kiểm tra thông báo
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Số lượng sản phẩm phải lớn hơn 0!')
        
        # Kiểm tra sản phẩm trong giỏ không thay đổi
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.count, 2)

    def test_update_cart_product_logged_in_exceeds_stock(self):
        response = self.client.post(self.update_cart_product_url, {
            'cart_id': self.cart.id,
            'cart_new_count': 15
        })
        
        # Kiểm tra chuyển hướng đến trang danh sách giỏ hàng
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart_list'))
        
        # Kiêm tra số lượng sản phẩm trong giỏ không thay đổi
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.count, 2)
        
    def test_update_cart_database_error(self):
        
        with self.assertRaises(Exception):
            with mock.patch('shop.views.Cart.objects.get', side_effect=Exception('Database error')):
                response = self.client.post(self.update_cart_product_url, {
                    'cart_id': self.cart.id,
                    'cart_new_count': 3
                })
                # Kiểm tra chuyển hướng đến trang danh sách giỏ hàng
                self.assertEqual(response.status_code, 302)
                self.assertRedirects(response, reverse('cart_list'))
        
                # Kiểm tra thông báo
                messages = list(get_messages(response.wsgi_request))
                self.assertEqual(len(messages), 1)
                self.assertEqual(str(messages[0]), 'Database error')
                
                self.cart.refresh_from_db()
                self.assertEqual(self.cart.count, 2)

# py manage.py test shop.tests.test_views_cart.UpdateCartProductViewTest
class CartProductDeleteViewTest(TestCase):
    
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
        
        # Tạo giỏ hàng, sản phẩm và danh mục tương ứng
        self.category = Category.objects.create(name='Test Category', decription='A test category description')
        self.product = Product.objects.create(name='Test Product', price=100, stock_number=10, category=self.category)
        self.cart = Cart.objects.create(user=self.user, product=self.product, count=2)
        
        self.delete_cart_product_url = reverse('delete_cart_product')
        self.cart_list_url = reverse('cart_list')
        
    def test_delete_cart_product_not_logged_in(self):
        # Kiểm tra user chưa đăng nhập
        self.client.logout()
        
        response = self.client.post(self.delete_cart_product_url, {'cart_id': self.cart.id, 'product_id': self.product.id})
        
        # Kiểm tra chuyển hướng đến trang đăng nhập
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        
    def test_delete_cart_product_logged_in(self):
        response = self.client.post(self.delete_cart_product_url, {'cart_id': self.cart.id, 'product_id': self.product.id})
        
        # Kiểm tra chuyển hướng đến trang danh sách giỏ hàng
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart_list'))
        
        # Kiểm tra thông báo
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Đã xóa sản phẩm khỏi giỏ hàng!')
        
        # Kiểm tra sản phẩm đã được xóa khỏi giỏ hàng
        with self.assertRaises(Cart.DoesNotExist):
            Cart.objects.get(pk=self.cart.id)
            
    def test_delete_cart_product_database_error(self):
        
        with self.assertRaises(Exception):
            with mock.patch('shop.views.Cart.objects.get', side_effect=Exception('Database error')):
                response = self.client.post(self.delete_cart_product_url, {'cart_id': self.cart.id, 'product_id': self.product.id})
                
                # Kiểm tra chuyển hướng đến trang danh sách giỏ hàng
                self.assertEqual(response.status_code, 302)
                self.assertRedirects(response, reverse('cart_list'))
                
                # Kiểm tra thông báo
                messages = list(get_messages(response.wsgi_request))
                self.assertEqual(len(messages), 1)
                self.assertEqual(str(messages[0]), 'Database error')
                # kiểm tra sản phẩm còn trong giỏ
                self.cart.refresh_from_db()
                self.assertEqual(self.cart.count, 2)

# py manage.py test shop.tests.test_views_cart.CartProductDeleteViewTest
class CheckoutCartViewTest(TestCase):
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
        
        # Tạo giỏ hàng, sản phẩm và danh mục tương ứng
        self.category = Category.objects.create(name='Test Category', decription='A test category description')
        self.product1 = Product.objects.create(name='Test Product', price=100, stock_number=10, category=self.category)
        self.product2 = Product.objects.create(name='Test Product 2', price=200, stock_number=20, category=self.category)
        self.cart1 = Cart.objects.create(user=self.user, product=self.product1, count=2)
        self.cart2 = Cart.objects.create(user=self.user, product=self.product2, count=1)
        
        self.checkout_cart_url = reverse('checkout_cart')
        self.cart_list_url = reverse('cart_list')
        
    def test_checkout_cart_not_logged_in(self):
        # Kiểm tra user chưa đăng nhập
        self.client.logout()
        
        response = self.client.post(self.checkout_cart_url)
        
        # Kiểm tra chuyển hướng đến trang đăng nhập
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        
    def test_checkout_cart_logged_in(self):
        response = self.client.post(self.checkout_cart_url)
        
        # Kiểm tra chuyển hướng đến trang danh sách giỏ hàng
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart_list'))
        
        # Kiểm tra thông báo
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Hóa đơn đã được thanh toán!')
        
        # Kiểm tra lượng sản phẩm tồn kho đã được cập nhật
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.stock_number, 8)
        self.assertEqual(self.product2.stock_number, 19)
        
        # Kiểm tra giỏ hàng đã được xóa
        self.assertEqual(Cart.objects.filter(user=self.user).count(), 0)
        
        # Kiểm tra lịch sử mua hàng
        history = History.objects.get(user=self.user)
        self.assertEqual(history.total_amount, 400)
        
    def test_checkout_cart_database_error(self):
        
        with self.assertRaises(Exception):
            with mock.patch('shop.views.Cart.objects.filter', side_effect=Exception('Database error')):
                response = self.client.post(self.checkout_cart_url)
                
                # Kiểm tra chuyển hướng đến trang danh sách giỏ hàng
                self.assertEqual(response.status_code, 302)
                self.assertRedirects(response, reverse('cart_list'))
                
                # Kiểm tra thông báo
                messages = list(get_messages(response.wsgi_request))
                self.assertEqual(len(messages), 1)
                self.assertEqual(str(messages[0]), 'Thanh toán thất bại!')

# py manage.py test shop.tests.test_views_cart.CheckoutCartViewTest

# py manage.py test shop.tests.test_views_cart