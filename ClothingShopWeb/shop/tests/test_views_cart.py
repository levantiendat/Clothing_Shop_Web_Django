from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Account
from shop.models import Category, Product, History, Cart
from django.utils import timezone
import json

class Test_Cart_Views(TestCase):
    
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


# py manage.py test shop