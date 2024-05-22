from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from shop.models import Category, Product, Cart, History
from accounts.models import Account
from django.utils import timezone

class TestShopModels(TestCase):

    def setUp(self):
        # tạo một người dùng thử nghiệm
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # tạo một danh mục thử nghiệm
        self.category = Category.objects.create(name='Test Category', decription='A test category description')
        # tạo một sản phẩm thử nghiệm
        self.product = Product.objects.create(name='Test Product', price=100, stock_number=50, category=self.category)
        # tạo một giỏ hàng thử nghiệm
        self.cart = Cart.objects.create(user=self.user, product=self.product, count=2)
        # tạo môt lịch sử giỏ hàng thử nghiệm
        self.history = History.objects.create(user=self.user, date=timezone.now(), total_amount=200)

    def test_category_creation(self):
        category = Category.objects.get(name='Test Category')
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.decription, 'A test category description')

    def test_product_creation(self):
        product = Product.objects.get(name='Test Product')
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.price, 100)
        self.assertEqual(product.stock_number, 50)
        self.assertEqual(product.category, self.category)

    def test_cart_creation(self):
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.user, self.user)
        self.assertEqual(cart.product, self.product)
        self.assertEqual(cart.count, 2)

    def test_history_creation(self):
        history = History.objects.get(user=self.user)
        self.assertEqual(history.user, self.user)
        self.assertEqual(history.total_amount, 200)

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Test Product')

    def test_cart_str(self):
        self.assertEqual(str(self.cart), 'testuser-Test Product-2')

    def test_history_str(self):
        self.assertTrue(str(self.history).startswith('testuser-'))

    def test_foreign_key_relationships(self): # kiểm tra quan hệ khóa ngoại

        self.assertEqual(self.product.category, self.category)
        
        self.assertEqual(self.cart.user, self.user)
        
        self.assertEqual(self.cart.product, self.product)
       
        self.assertEqual(self.history.user, self.user)
 
# py manage.py test shop.tests.test_models