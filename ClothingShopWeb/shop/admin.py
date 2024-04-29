from django.contrib import admin
from .models import Category
from .models import Product
from .models import Cart
from .models import History

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(History)



