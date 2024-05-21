from django.test import SimpleTestCase
from django.urls import reverse, resolve
from shop.views import category_list, product_list, cart_list, personal_list
from shop.views import cart_update, add_cart, update_cart_product, delete_cart_product, checkout_cart, history_list
from shop.views import add_category, category_update, category_update_accept, category_delete
from shop.views import add_product, product_update_accept, product_delete, product_update, product_list_category
from shop.views import personal_info, update_personal_info, delete_user, personal_list_update_view, update_personal_list_info

class TestShopUrls(SimpleTestCase):
    
    def test_category_list_url_resolves(self):
        url = reverse('category_list')
        self.assertEqual(resolve(url).func, category_list)
        
    def test_product_list_url_resolves(self):
        url = reverse('product_list')
        self.assertEqual(resolve(url).func, product_list)
        
    def test_cart_list_url_resolves(self):
        url = reverse('cart_list')
        self.assertEqual(resolve(url).func, cart_list)
        
    def test_cart_update_url_resolves(self):
        url = reverse('cart_update')
        self.assertEqual(resolve(url).func, cart_update)
        
    def test_add_cart_url_resolves(self):
        url = reverse('add_cart')
        self.assertEqual(resolve(url).func, add_cart)
    
    def test_update_cart_product_url_resolves(self):
        url = reverse('update_cart_product')
        self.assertEqual(resolve(url).func, update_cart_product)
        
    def test_delete_cart_product_url_resolves(self):
        url = reverse('delete_cart_product')
        self.assertEqual(resolve(url).func, delete_cart_product)
        
    def test_checkout_cart_url_resolves(self):
        url = reverse('checkout_cart')
        self.assertEqual(resolve(url).func, checkout_cart)
    
    def test_add_category_url_resolves(self):
        url = reverse('add_category')
        self.assertEqual(resolve(url).func, add_category)
    
    def test_add_product_url_resolves(self):
        url = reverse('add_product')
        self.assertEqual(resolve(url).func, add_product)
        
    def test_product_list_category_url_resolves(self):
        url = reverse('product_list_category', args=[1])
        self.assertEqual(resolve(url).func, product_list_category)
        
    def test_history_list_url_resolves(self):
        url = reverse('history_list')
        self.assertEqual(resolve(url).func, history_list)
        
    def test_category_update_url_resolves(self):
        url = reverse('category_update', args=[1])
        self.assertEqual(resolve(url).func, category_update)
        
    def test_category_update_accept_url_resolves(self):
        url = reverse('category_update_accept')
        self.assertEqual(resolve(url).func, category_update_accept)
        
    def test_category_delete_url_resolves(self):
        url = reverse('category_delete', args=[1])
        self.assertEqual(resolve(url).func, category_delete)
        
    def test_product_update_url_resolves(self):
        url = reverse('product_update', args=[1])
        self.assertEqual(resolve(url).func, product_update)
        
    def test_product_update_accept_url_resolves(self):
        url = reverse('product_update_accept')
        self.assertEqual(resolve(url).func, product_update_accept)
        
    def test_product_delete_url_resolves(self):
        url = reverse('product_delete', args=[1])
        self.assertEqual(resolve(url).func, product_delete)
        
    def test_personal_info_url_resolves(self):
        url = reverse('Personal')
        self.assertEqual(resolve(url).func, personal_info)
        
    def test_update_personal_info_url_resolves(self):
        url = reverse('update_personal_info')
        self.assertEqual(resolve(url).func, update_personal_info)
        
    def test_personal_list_url_resolves(self):
        url = reverse('personal_list')
        self.assertEqual(resolve(url).func, personal_list)
        
    def test_personal_delete_url_resolves(self):
        url = reverse('personal_delete', args=['id'])
        self.assertEqual(resolve(url).func, delete_user)
        
    def test_personal_list_update_view_url_resolves(self):
        url = reverse('personal_list_update_view', args=['id'])
        self.assertEqual(resolve(url).func, personal_list_update_view)
        
    def test_update_personal_list_info_url_resolves(self):
        url = reverse('update_personal_list_info', args=['id'])
        self.assertEqual(resolve(url).func, update_personal_list_info)
        
       
# py manage.py test shop