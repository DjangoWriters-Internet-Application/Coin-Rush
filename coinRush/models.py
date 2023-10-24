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

class Transaction(models.Model):
    TYPE = [('BUY', 'Buy'), ('SELL', 'Sell')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10,choices=TYPE, default='BUY')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.transaction_type}{self.quantity} {self.stock.symbol} @ {self.price}"

class UserHolding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.email} - {self.quantity} {self.stock.symbol}"


class News(models.Model):
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    # image = models.ImageField(upload_to='news_images/')
    description = models.TextField(max_length=1000)
    publish_datetime = models.DateTimeField()

    def __str__(self):
        return self.title

class Learn(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    external_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class NFT(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('BTC', 'Bitcoin'),
        ('ETH', 'Ethereum'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='nft_images/')
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    is_for_sale = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    is_bidding_allowed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.owner

class Bid(models.Model):
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.bidder
