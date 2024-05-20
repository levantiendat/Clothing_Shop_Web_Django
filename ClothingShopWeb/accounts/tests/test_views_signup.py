from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Account
import json

class TestViews(TestCase):
    
    def test_signup_POST(self): # đăng nhập thành công
        client = Client()
        response = client.post(reverse('signup'), {
            'username': 'testuser',
            'name': 'testname',
            'email': 'test@gmail.com',
            'phone_number': '0123456789',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'role': 0
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.first().username, 'testuser')
        self.assertTrue(User.objects.first().check_password('testpassword'))
        self.assertEqual(User.objects.first().email, 'test@gmail.com')
        self.assertEqual(Account.objects.first().name, 'testname')
        self.assertEqual(Account.objects.first().phone_number, '0123456789')
        self.assertEqual(Account.objects.first().role, 0)

        self.assertEqual(response.url, '/accounts/login/')
        
    def test_signup_POST_no_email(self): # đăng nhập thành công không có email
        client = Client()
        response = client.post(reverse('signup'), {
            'username': 'testuser',
            'name': 'testname',
            'email': '',
            'phone_number': '0123456789',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'role': 0
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.first().username, 'testuser')
        self.assertTrue(User.objects.first().check_password('testpassword'))
        self.assertEqual(User.objects.first().email, '')
        self.assertEqual(Account.objects.first().name, 'testname')
        self.assertEqual(Account.objects.first().phone_number, '0123456789')
        self.assertEqual(Account.objects.first().role, 0)

        self.assertEqual(response.url, '/accounts/login/')
        
    def test_signup_POST_fail_password_like_username(self): # mật khẩu giống tên người dùng
        client = Client()
        response = client.post(reverse('signup'), {
            'username': 'testpassword',
            'name': 'testname',
            'email': 'test@gmail.com',
            'phone_number': '0123456789',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'role': 0
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        
    def test_signup_POST_fail_password_like_email(self): # mật khẩu giống email
        client = Client()
        response = client.post(reverse('signup'), {
            'username': 'testuser',
            'name': 'testname',
            'email': 'testpassword@gmail.com',
            'phone_number': '0123456789',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'role': 0
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
    
    def test_signup_POST_fail_password_all_number(self): # mật khẩu chỉ có số
        client = Client()
        response = client.post(reverse('signup'), {
            'username': 'testuser',
            'name': 'testname',
            'email': 'test@gmail.com',
            'phone_number': '0123456789',
            'password1': '11111111',
            'password2': '11111111',
            'role': 0
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
    
    def test_signup_POST_fail_password_too_short(self): # mật khẩu quá ngắn
        client = Client()
        response = client.post(reverse('signup'), {
            'username': 'testuser',
            'name': 'testname',
            'email': 'test@gmail.com',
            'phone_number': '0123456789',
            'password1': 'tespwd1',
            'password2': 'tespwd1',
            'role': 0
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
    
    def test_signup_POST_fail_mismatch_password(self): # mật khẩu không khớp
        client = Client()
        response = client.post(reverse('signup'), {
            'username': 'testuser',
            'name': 'testname',
            'email': 'test@gmail.com',
            'phone_number': '0123456789',
            'password1': 'testpassword',
            'password2': 'testpassword1',
            'role': 0
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        
    def test_signup_POST_fail_simple_password(self): # mật khẩu quá đơn giản
        client = Client()
        response = client.post(reverse('signup'), {
            'username': 'testuser',
            'name': 'testname',
            'email': 'test@gmail.com',
            'phone_number': '0123456789',
            'password1': 'password',
            'password2': 'password',
            'role': 0
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        
    def test_signup_POST_fail_empty_password1(self): # mật khẩu trống
        client = Client()
        response = client.post(reverse('signup'), {
            'username': 'testuser',
            'name': 'testname',
            'email': 'test@gmail.com',
            'phone_number': '0123456789',
            'password1': '',
            'password2': 'testpassword',
            'role': 0
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_POST_fail_empty_password2(self): # mật khẩu lần 2 trống
        client = Client()
        response = client.post(reverse('signup'), {
            'username': 'testuser',
            'name': 'testname',
            'email': 'test@gmail.com',
            'phone_number': '0123456789',
            'password1': 'testpassword',
            'password2': '',
            'role': 0
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
    
    def test_signup_POST_fail_empty_username(self): # tên người dùng trống
        client = Client()
        response = client.post(reverse('signup'), {
            'username': '',
            'name': 'testname',
            'email': 'test@gmail.com',
            'phone_number': '0123456789',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'role': 0
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_POST_fail_empty_name(self): # tên trống
        client = Client()
        response = client.post(reverse('signup'), {
            'username': 'testuser',
            'name': '',
            'email': 'test@gmail.com',
            'phone_number': '0123456789',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'role': 0
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        
    def test_signup_POST_fail_empty_phone(self): # số điện thoại trống
        client = Client()
        response = client.post(reverse('signup'), {
            'username': 'testuser',
            'name': 'testname',
            'email': 'test@gmail.com',
            'phone_number': '',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'role': 0
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        
    def test_signup_POST_fail_user_exits(self): # người dùng đã tồn tại
        client = Client()
        response = client.post(reverse('signup'), {
            'username': 'testuser',
            'name': 'testname',
            'email': '',
            'phone_number': '0123456789',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'role': 0
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.first().username, 'testuser')
        self.assertTrue(User.objects.first().check_password('testpassword'))
        self.assertEqual(User.objects.first().email, '')
        self.assertEqual(Account.objects.first().name, 'testname')
        self.assertEqual(Account.objects.first().phone_number, '0123456789')
        self.assertEqual(Account.objects.first().role, 0)

        self.assertEqual(response.url, '/accounts/login/')
        
        client2 = Client()
        response = client2.post(reverse('signup'), {
            'username': 'testuser',
            'name': 'testname1',
            'email': 'test@gmail.com',
            'phone_number': '5678901234',
            'password1': 'passwordtest',
            'password2': 'passwordtest',
            'role': 0
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

# py manage.py test accounts