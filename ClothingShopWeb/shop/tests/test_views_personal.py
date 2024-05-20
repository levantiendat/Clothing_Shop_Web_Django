from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Account
from shop.models import Category, Product, History, Cart
from django.utils import timezone
import json

class PersonalInfoViewTest(TestCase):
    def setUp(self):
        # Tạo user và account tương ứng
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.login_url = reverse('login')  # Thay thế 'login' bằng tên đường dẫn của trang đăng nhập của bạn
        self.personal_info_url = reverse('Personal')  # Thay thế 'Personal' bằng tên đường dẫn của trang thông tin cá nhân
        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)
        
        # Đăng nhập
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })

    def test_personal_info_view_authenticated(self):
        # Test khi user đã đăng nhập thành công và có quyền truy cập
        response = self.client.get(self.personal_info_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personal.html')
        self.assertEqual(response.context['user'], self.account)

    def test_personal_info_view_not_authenticated(self):
        # Test khi user chưa đăng nhập
        self.client.logout()
        # Đổi username trong session để giả lập user chưa đăng nhập
        response = self.client.get(self.personal_info_url)
        
        self.assertEqual(response.status_code, 302)  # Chuyển hướng đến trang đăng nhập
        self.assertRedirects(response, self.login_url)
        
class PersonalListViewTest(TestCase):
    def setUp(self):
        # Tạo user và account tương ứng
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.login_url = reverse('login')  # Thay thế 'login' bằng tên đường dẫn của trang đăng nhập của bạn
        self.personal_list_url = reverse('personal_list')  # Thay thế 'Personal' bằng tên đường dẫn của trang thông tin cá nhân
        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)
        # Tạo thêm một số Account khác
        self.account1 = Account.objects.create(user=User.objects.create_user(username='user1', password='password1'), name='User One', phone_number='1111111111', role=2)
        self.account2 = Account.objects.create(user=User.objects.create_user(username='user2', password='password2'), name='User Two', phone_number='2222222222', role=3)
        # Đăng nhập
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })
        
    def test_personal_info_view_authenticated(self):
        # Test khi user đã đăng nhập thành công và có quyền truy cập
        response = self.client.get(self.personal_list_url)
        
        # Kiểm tra xem view trả về đúng template và context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personal_list.html')
        
        # Kiểm tra context có chứa đúng thông tin của người dùng hiện tại và danh sách tất cả các tài khoản
        self.assertIn('user', response.context)
        self.assertIn('users', response.context)
        self.assertEqual(response.context['user'], self.account)
        self.assertEqual(len(response.context['users']), Account.objects.count())
        # Kiểm tra danh sách các tài khoản dựa trên ID
        expected_users = [self.account, self.account1, self.account2]
        actual_users = list(response.context['users'])
        self.assertCountEqual(
            [user.pk for user in actual_users],
            [user.pk for user in expected_users]
        )
        
    def test_personal_list_view_not_authenticated(self):
        # Test khi user chưa đăng nhập
        self.client.logout()
        # Đổi username trong session để giả lập user chưa đăng nhập
        response = self.client.get(self.personal_list_url)
        
        self.assertEqual(response.status_code, 302)  # Chuyển hướng đến trang đăng nhập
        self.assertRedirects(response, self.login_url)

# py manage.py test shop