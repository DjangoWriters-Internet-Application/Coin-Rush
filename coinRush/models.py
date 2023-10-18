from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.db import models
from django.conf import settings

from .managers import AuthUserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(default="", unique=True, blank=True, max_length=255)
    name = models.CharField(max_length=255, blank=True, default="")

    profile_pic = models.ImageField(null=True, blank=True)
    photo_id = models.ImageField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    created_date = models.DateTimeField(default=timezone.now())
    last_login = models.DateTimeField(blank=True, null=True)

    objects = AuthUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUERIES_FIELD = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.email.split("@")[0]



class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    post_comments = models.ManyToManyField('Comment', related_name='post_comments', blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.created_by.username}"


# Define a model for Stock
class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=255)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    market_cap = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol

# Define a model for StockPrice (to store historical price data)
class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.stock.symbol} - {self.date}"
