from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Account
import json

class Test_Login_Views(TestCase):
    
    def setUp(self):
        # Tạo một user mới để test
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_url = reverse('login') 
        self.category_list_url = reverse('category_list')
        # Tạo một account để test
        Account.objects.create(user=self.user, name='testname', phone_number='0123456789', role=0)

    def test_successful_login(self): # đăng nhập thành công

        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })
        self.assertRedirects(response, self.category_list_url)
        self.assertIn('user', self.client.session)
        self.assertEqual(self.client.session['user'], self.username)

    def test_unsuccessful_login_wrong_pass(self): # đăng nhập thất bại với mật khẩu sai

        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn('_auth_user_id', self.client.session)
    
    def test_unsuccessful_login_wrong_username(self):

        response = self.client.post(self.login_url, {
            'username': 'wrongusername',
            'password': self.password,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertNotIn('_auth_user_id', self.client.session)
        
# py manage.py test accounts.tests.test_view_login