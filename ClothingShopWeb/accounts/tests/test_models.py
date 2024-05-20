from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Account

class TestAccountModel(TestCase):

    def setUp(self):
        # Tạo một user thử nghiệm
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Tạo một đối tượng Account thử nghiệm
        self.account = Account.objects.create(user=self.user, name='Test User', phone_number='1234567890', role=1)

    def test_account_creation(self):
        # Test tạo đối tượng Account thành công
        self.assertIsInstance(self.account, Account)
        self.assertEqual(self.account.name, 'Test User')
        self.assertEqual(self.account.phone_number, '1234567890')
        self.assertEqual(self.account.role, 1)

    def test_account_str_method(self):
        # Test phương thức __str__ của Account
        self.assertEqual(str(self.account), 'testuser')

    def test_account_user_relationship(self):
        # Test mối quan hệ OneToOneField với User
        self.assertEqual(self.account.user, self.user)
        self.assertEqual(self.user.account, self.account)  # Xác thực ngược lại
        
# py manage.py test accounts