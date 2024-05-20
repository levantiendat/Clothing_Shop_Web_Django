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

# py manage.py test shop