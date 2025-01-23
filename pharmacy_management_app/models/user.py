import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from ..models.product import Product
from ..models.purchase import Purchase

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def create_admin_from_env(self):
        email = settings.ADMIN_EMAIL    
        password = settings.ADMIN_PASSWORD
        if not self.filter(email=email).exists():
            self.create_superuser(email=email, password=password)

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    purchased_products = models.ManyToManyField(Product, through=Purchase, related_name='buyers')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email



