from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Account
from shop.models import Category, Product, History, Cart
from django.utils import timezone
import json



# py manage.py test shop