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
        self.login_url = reverse('login')  # Thay thế 'login' bằng tên đường dẫn của trang đăng nhập của bạn
        self.category_list_url = reverse('category_list')  # Thay thế 'category_list' bằng tên đường dẫn của view category_list
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

    def test_category_list_view_authenticated(self):
        
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
        # Create a user and corresponding account
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.login_url = reverse('login')  # Replace 'login' with the actual name of your login URL
        self.add_category_url = reverse('add_category')  # Replace 'add_category' with the actual name of your add category URL

        # Create account for the user
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
        
# py manage.py test shop