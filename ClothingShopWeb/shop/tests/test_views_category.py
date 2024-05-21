from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Account
from shop.models import Category, Product, History, Cart
from django.utils import timezone
import json

class CategoryListViewTest(TestCase):
    def setUp(self):
        # Tạo user và account tương ứng
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.login_url = reverse('login')
        self.category_list_url = reverse('category_list')
        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)
        
        # Tạo thêm một số Category
        self.category1 = Category.objects.create(name='Category One', decription='Description One')
        self.category2 = Category.objects.create(name='Category Two', decription='Description Two')
        
        # Đăng nhập
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })
        
    def test_category_list_view_not_authenticated(self):
        # Test khi user chưa đăng nhập
        self.client.logout()

        response = self.client.get(self.category_list_url)
        
        self.assertEqual(response.status_code, 302)  # Chuyển hướng đến trang đăng nhập
        self.assertRedirects(response, self.login_url)

    def test_category_list_view_get_authenticated(self):
        
        response = self.client.get(self.category_list_url)
        
        # Kiểm tra xem view trả về đúng template và context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_list.html')
        
        # Kiểm tra context có chứa đúng thông tin của người dùng hiện tại và danh sách tất cả các danh mục
        self.assertIn('user', response.context)
        self.assertIn('categories', response.context)
        self.assertEqual(response.context['user'], self.account)

        # Kiểm tra danh sách các danh mục dựa trên ID
        expected_categories = [self.category1, self.category2]
        actual_categories = list(response.context['categories'])
        self.assertCountEqual(
            [category.pk for category in actual_categories],
            [category.pk for category in expected_categories]
        )

class AddCategoryViewTest(TestCase):
    def setUp(self):
        # Tạo user và account tương ứng
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.login_url = reverse('login')
        self.add_category_url = reverse('add_category')
        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)
        
        # Đăng nhập
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })

    def test_add_category_view_not_authenticated(self):
        # Test khi user chưa đăng nhập
        self.client.logout()
        
        response = self.client.get(self.add_category_url)
        
        # Kiểm tra xem có chuyển hướng đến trang đăng nhập không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_add_category_view_get_authenticated(self):
        
        response = self.client.get(self.add_category_url)
        
        # Kiểm tra xem view trả về đúng template và context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_category.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.account)

    def test_add_category_view_post_authenticated_success(self):

        category_data = {
            'category_name': 'New Category',
            'decription': 'Description for new category'
        }
        
        response = self.client.post(self.add_category_url, category_data)
        
        # Kiểm tra xem có chuyển hướng đến trang danh sách danh mục không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('category_list'))
        
        # Kiểm tra xem danh mục đã được tạo thành công chưa
        category_exists = Category.objects.filter(name='New Category').exists()
        self.assertTrue(category_exists)

    def test_add_category_view_post_authenticated_failure(self):

        # Thử tạo một danh mục mới với tên rỗng
        category_data = {
            'decription': 'Description without name'
        }
        
        response = self.client.post(self.add_category_url, category_data)
        
        # Kiểm tra xem view trả về đúng template và context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_category.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.account)
        # Kiểm tra xem có hiển thị thông báo lỗi không
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'Thêm thất bại!')

class CategoryUpdateViewTest(TestCase):
    def setUp(self):
        # Tạo user và account tương ứng
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.login_url = reverse('login')
        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)
        
        # Tạo một danh mục thử nghiệm
        self.category = Category.objects.create(name='Test Category', decription='Test Description')
        category_id = int(self.category.id)
        self.category_update_url = reverse('category_update', args=[category_id])
        
        # Đăng nhập
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })
        
    def test_category_update_view_not_authenticated(self):
        # Test khi user chưa đăng nhập
        self.client.logout()
        
        response = self.client.get(self.category_update_url)
        
        # Kiểm tra có chuyển hướng đến trang đăng nhập không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_category_update_view_get_authenticated(self):
        
        response = self.client.get(self.category_update_url)
        
        # Kiểm tra có trả về đúng template và context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_update.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.account)
        self.assertIn('category', response.context)
        self.assertEqual(response.context['category'], self.category)
        
class CategoryUpdateAcceptViewTest(TestCase):
    def setUp(self):
        # Tạo user và account tương ứng
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.login_url = reverse('login')
        self.category_update_accept_url = reverse('category_update_accept')
        self.category_list_url = reverse('category_list')

        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)
        
        # Tạo một danh mục thử nghiệm
        self.category = Category.objects.create(name='Test Category', decription='Test Description')
        
        # Đăng nhập
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })

    def test_category_update_accept_view_not_authenticated(self):
        # Kiểm tra khi user chưa đăng nhập
        self.client.logout()
        
        response = self.client.post(self.category_update_accept_url, {
            'category_id': self.category.id,
            'category_name': 'Updated Category',
            'decription': 'Updated Description'
        })
        
        # Kiểm tra có chuyển hướng đến trang đăng nhập không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_category_update_accept_view_authenticated_valid_data(self):

        response = self.client.post(self.category_update_accept_url, {
            'category_id': self.category.id,
            'category_name': 'Updated Category',
            'decription': 'Updated Description'
        })
        
        # Kiểm tra xem danh mục đã được cập nhật thành công chưa
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')
        self.assertEqual(self.category.decription, 'Updated Description')

        # Kiểm tra có chuyển hướng đến trang danh sách danh mục không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.category_list_url)

    def test_category_update_accept_view_authenticated_invalid_data(self):

        # Cố ý gửi dữ liệu không hợp lệ
        response = self.client.post(self.category_update_accept_url, {
            'category_id': self.category.id,
            'category_name': '',
            'decription': 'Updated Description'
        })

        # Kiểm tra xem danh mục đã được cập nhật chưa
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Thêm thất bại!')

        # Kiểm tra có chuyển hướng đến trang danh sách danh mục không
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_update.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.account)
        self.assertIn('category', response.context)
        self.assertEqual(response.context['category'], self.category)
    
    def test_category_update_accept_view_database_error(self):
            
            # Tạo một lỗi cơ sở dữ liệu bằng cách cố gắng cập nhật một danh mục không tồn tại
            with self.assertRaises(Exception):
                with mock.patch('shop.models.Account.save', side_effect=Exception('Database error')):
                    response = self.client.post(self.category_update_accept_url, {
                        'category_id': self.category.id,
                        'category_name': 'Updated Category',
                        'decription': 'Updated Description'
                    })
                    # Kiểm tra có chuyển hướng đến trang danh sách danh mục không
                    self.assertEqual(response.status_code, 302)
                    self.assertRedirects(response, self.category_list_url)
    
            # Kiểm tra xem danh mục đã được cập nhật chưa
            self.category.refresh_from_db()
            self.assertEqual(self.category.name, 'Test Category')
            self.assertEqual(self.category.decription, 'Test Description')
        
class CategoryDeleteViewTest(TestCase):

    def setUp(self):
        # Create a user and account
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.login_url = reverse('login')
        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)
        
        # Tạo một danh mục
        self.category = Category.objects.create(name='Test Category', decription='Test Description')
        
        # Tạo một sản phẩm thuộc danh mục
        self.product = Product.objects.create(name='Test Product', category=self.category, price=10.00, stock_number=100)
        
        # Tạo một giỏ hàng chứa sản phẩm
        self.cart = Cart.objects.create(product=self.product, count=1, user=self.user)

        self.category_delete_url = reverse('category_delete', args=[self.category.id])
        
        # Đăng nhập
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })
    
    def test_category_delete_not_authenticated(self):
        # Kiêm tra khi user chưa đăng nhập
        self.client.logout()

        response = self.client.get(self.category_delete_url)

        # Kiểm tra có chuyển hướng đến trang đăng nhập không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_category_delete_successful(self):

        response = self.client.get(self.category_delete_url)

        # Kiểm tra có chuyển hướng đến trang danh sách danh mục không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('category_list'))

        # Kiểm tra xem danh mục đã bị xóa chưa
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
        self.assertFalse(Cart.objects.filter(id=self.cart.id).exists())


# py manage.py test shop