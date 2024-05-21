from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Account
from shop.models import Category, Product, History, Cart
from shop.views import Check_Phone
from django.utils import timezone
import json

class PersonalInfoViewTest(TestCase):
    def setUp(self):
        # Tạo user và account tương ứng
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.login_url = reverse('login')
        self.personal_info_url = reverse('Personal')
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
        self.login_url = reverse('login')
        self.personal_list_url = reverse('personal_list')
        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)
        # Tạo thêm một số Account khác
        self.account1 = Account.objects.create(user=User.objects.create_user(username='user1', password='password1'), name='User One', phone_number='1111111111', role=0)
        self.account2 = Account.objects.create(user=User.objects.create_user(username='user2', password='password2'), name='User Two', phone_number='2222222222', role=1)
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
        
        response = self.client.get(self.personal_list_url)
        
        self.assertEqual(response.status_code, 302)  # Chuyển hướng đến trang đăng nhập
        self.assertRedirects(response, self.login_url)

class CheckPhoneViewTest(TestCase):

    def test_valid_phone_number(self):
        # Kiểm tra với số điện thoại hợp lệ
        phone_number = '1234567890'
        self.assertTrue(Check_Phone(phone_number))

    def test_invalid_phone_number(self):
        # Kiểm tra với số điện thoại không hợp lệ (ít hơn 10 chữ số)
        phone_number = '123456789'
        self.assertFalse(Check_Phone(phone_number))

        # Kiểm tra với số điện thoại không hợp lệ (nhiều hơn 10 chữ số)
        phone_number = '12345678901'
        self.assertFalse(Check_Phone(phone_number))

        # Kiểm tra với số điện thoại không hợp lệ (chứa ký tự không phải số)
        phone_number = '12345678A0'
        self.assertFalse(Check_Phone(phone_number))

        # Kiểm tra với số điện thoại không hợp lệ (chứa ký khoảng trắng)
        phone_number = '123 456 7890'
        self.assertFalse(Check_Phone(phone_number))

        # Kiểm tra với số điện thoại không hợp lệ (chứa ký tự đặc biệt)
        phone_number = '123-456-7890'
        self.assertFalse(Check_Phone(phone_number))

        # Kiểm tra với số điện thoại không hợp lệ (rỗng)
        phone_number = ''
        self.assertFalse(Check_Phone(phone_number))

    def test_edge_cases(self):

        # Kiểm tra với số điện thoại chính xác 10 chữ số
        phone_number = '1234567890'
        self.assertTrue(Check_Phone(phone_number))

        # Kiểm tra với số điện thoại chính xác 10 chữ số có khoảng trắng
        phone_number = '123 456 7890'
        self.assertFalse(Check_Phone(phone_number))

        # Kiểm tra với số điện thoại chính xác 10 chữ số có ký tự đặc biệt
        phone_number = '123-456-7890'
        self.assertFalse(Check_Phone(phone_number))

class UpdatePersonalInfoViewTest(TestCase):
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
        
        self.personal_info_url = reverse('Personal')
        
    def test_update_personal_info_not_authenticated(self):
        # Test khi user chưa đăng nhập
        self.client.logout()
        
        response = self.client.get(self.personal_info_url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        
    def test_update_personal_info_success(self):
        url = reverse('update_personal_info')
        data = {
            'Name': 'Updated Name',
            'Phone': '9876543210',
            'Role': 1,
            'user_id': self.user.username
        }
        response = self.client.post(url, data)
        
        # kiểm tra xem cập nhật thông tin có thành công không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.personal_info_url )
        
        # Chuyển hướng về đường dẫn Personal
        response = self.client.get(self.personal_info_url )
        # kiểm tra thông báo trả về
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Cập nhật thông tin thành công!')

        # Kiểm tra thông tin đã được cập nhật trong database
        self.account.refresh_from_db()
        self.assertEqual(self.account.name, 'Updated Name')
        self.assertEqual(self.account.phone_number, '9876543210')
        self.assertEqual(self.account.role, 1)

    def test_update_personal_info_database_error(self):
        
        url = reverse('update_personal_info')
        data = {
            'Name': 'Updated Name',
            'Phone': '9876543210',
            'Role': 0,
            'user_id': self.user.username
        }

        # mô phỏng lỗi khi lưu thông tin vào database
        with self.assertRaises(Exception):
            with mock.patch('shop.models.Account.save', side_effect=Exception('Database error')):
                response = self.client.post(url, data)
                # kiểm tra có chuyển hướng về Personal không
                self.assertEqual(response.status_code, 302)
                self.assertRedirects(response, self.personal_info_url )

        # Kiểm tra thông tin không thay đổi trong database
        self.account.refresh_from_db()
        self.assertNotEqual(self.account.name, 'Updated Name')
        self.assertNotEqual(self.account.phone_number, '9876543210')
        self.assertNotEqual(self.account.role, 0)

class UpdatePersonalListInfoViewTest(TestCase):
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
        
        self.personal_list_update_view_url = reverse('personal_list_update_view', kwargs={'user_id': self.user.username})
        self.update_personal_list_info_url = reverse('update_personal_list_info', kwargs={'user_id': self.user.username})
        
    def test_update_personal_list_info_success(self):
        data = {
            'Name': 'Updated Name',
            'Phone': '9876543210',
            'Role': 1,
            'user_id': self.user.username
        }
        response = self.client.post(self.update_personal_list_info_url, data)
        
        # kiểm tra xem cập nhật thông tin có thành công không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.personal_list_update_view_url)
        
        # Chuyển hướng về đường dẫn
        response = self.client.get(self.personal_list_update_view_url)
        # kiểm tra thông báo trả về
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Cập nhật thông tin thành công!')

        # Kiểm tra thông tin đã được cập nhật trong database
        self.account.refresh_from_db()
        self.assertEqual(self.account.name, 'Updated Name')
        self.assertEqual(self.account.phone_number, '9876543210')
        self.assertEqual(self.account.role, 1)
        
    def test_update_personal_list_info_database_error(self):
        data = {
            'Name': 'Updated Name',
            'Phone': '9876543210',
            'Role': 0,
            'user_id': self.user.username
        }

        # mô phỏng lỗi khi lưu thông tin vào database
        with self.assertRaises(Exception):
            with mock.patch('shop.models.Account.save', side_effect=Exception('Database error')):
                response = self.client.post(self.personal_list_update_view_url, data)
                # kiểm tra có chuyển hướng về Personal không
                self.assertEqual(response.status_code, 302)
                self.assertRedirects(response, self.personal_list_update_view_url)

        # Kiểm tra thông tin không thay đổi trong database
        self.account.refresh_from_db()
        self.assertNotEqual(self.account.name, 'Updated Name')
        self.assertNotEqual(self.account.phone_number, '9876543210')
        self.assertNotEqual(self.account.role, 0)

class PersonalListUpdateViewViewTest(TestCase):
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
        
        self.personal_list_update_view_url = reverse('personal_list_update_view', kwargs={'user_id': self.user.username})
    
    def test_personal_list_update_view(self):
        response = self.client.get(self.personal_list_update_view_url)
        
        self.assertEqual(response.status_code, 200)
        
        # Kiểm tra template và context
        self.assertTemplateUsed(response, 'personal_update.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.account)

class PersonalDeleteViewTest(TestCase):
    def setUp(self):
        # Tạo user và account tương ứng
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)
        
        self.user2= User.objects.create_user(username='user2', password=self.password)
        self.account2 = Account.objects.create(user=self.user2, name='User 2 Delete', phone_number='1234567890', role=1)
        
        # Đăng nhập
        self.client = Client()
        self.login_url = reverse('login')
        
        self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })
        
        self.personal_delete_url = reverse('personal_delete', kwargs={'user_id': self.user2.username})
        
    def test_personal_delete_view_not_authenticated(self):
        # Kiêm tra khi user chưa đăng nhập
        self.client.logout()
        
        response = self.client.get(self.personal_delete_url)
        
        # Kiểm tra có chuyển hướng đến trang đăng nhập không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
            
    def test_personal_delete_successful(self):
        response = self.client.post(self.personal_delete_url)
        
        # Kiểm tra có chuyển hướng về trang danh sách tài khoản không
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('personal_list'))

        # Kiểm tra tài khoản đã bị xóa khỏi database
        self.assertFalse(Account.objects.filter(user=self.user2).exists())

# py manage.py test shop