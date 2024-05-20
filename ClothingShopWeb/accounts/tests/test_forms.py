from django.test import TestCase
from django.contrib.auth.models import User
from accounts.forms import CustomUserCreationForm
from accounts.models import Account

class FormTest(TestCase):

    def test_custom_user_creation_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'name': 'Test User',
            'phone_number': '1234567890',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_form(self):
        form = CustomUserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['This field is required.'])
        self.assertEqual(form.errors['name'], ['This field is required.'])
        self.assertEqual(form.errors['phone_number'], ['This field is required.'])
        self.assertEqual(form.errors['password1'], ['This field is required.'])
        self.assertEqual(form.errors['password2'], ['This field is required.'])

    def test_invalid_phone_number(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'name': 'Test User',
            'phone_number': '123456789009876543210',  # Số điện thoại không hợp lệ
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['phone_number'], ['Ensure this value has at most 20 characters (it has 21).'])

    def test_passwords_not_match(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'name': 'Test User',
            'phone_number': '1234567890',
            'password1': 'testpassword',
            'password2': 'differentpassword',  # Passwords không khớp nhau
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ["The two password fields didn’t match."])

    def test_create_user(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'name': 'Test User',
            'phone_number': '0123456789',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')

# py manage.py test accounts