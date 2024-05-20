from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Account
from shop.models import Category, Product, History, Cart
from django.utils import timezone
import json
    
class Test_Category_Views(TestCase):
    
    def setUp(self):
        # Tạo một user mới để test
        self.username = 'testuser'


# py manage.py test shop