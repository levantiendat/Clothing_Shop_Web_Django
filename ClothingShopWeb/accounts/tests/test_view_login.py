from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Account
import json

class TestViews(TestCase):
    
    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_url = reverse('login')  # Assuming the URL name for the login view is 'user_login'
        self.category_list_url = reverse('category_list')

# py manage.py test accounts