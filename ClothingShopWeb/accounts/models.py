from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=False)
    phone_number = models.CharField(max_length=10, blank=False)
    role = models.IntegerField()

    def __str__(self):
        return self.user.username
