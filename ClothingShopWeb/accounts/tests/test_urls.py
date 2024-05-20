from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import signup, user_login

class TestAccountUrls(SimpleTestCase):
    
    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, signup)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, user_login)
        
# py manage.py test accounts