from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.db import models
from django.conf import settings
from .managers import AuthUserManager
from django.forms import ModelForm
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(default="", unique=True, blank=True, max_length=255)
    name = models.CharField(max_length=255, blank=True, default="")
    password = models.CharField(max_length=255)

    profile_pic = models.TextField(null=True, blank=True, default="")
    photo_id = models.TextField(null=True, blank=True, default="")

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    created_date = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    liked_news = models.ManyToManyField("News", blank=True, null=True)

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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.created_by.name}"


# Define a model for Stock
class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=255)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    market_cap = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="stock_pics/", blank=True, null=True)

    def __str__(self):
        return self.symbol


class NFT(models.Model):
    CURRENCY_CHOICES = [
        ("USD", "US Dollar"),
        ("BTC", "Bitcoin"),
        ("ETH", "Ethereum"),
    ]

    symbol = models.CharField(max_length=15, blank=True)
    company_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="nft_images/")
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    is_for_sale = models.BooleanField(default=False)
    current_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="USD")


    def __str__(self):
        return self.symbol


class NFTTransaction(models.Model):
    TYPE_CHOICES = [
        ("BUY", "Buy"),
        ("SELL", "Sell"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, default="BUY"
    )
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.transaction_type} {self.quantity} {self.nft.symbol} @ {self.price}"


class NFTUserHolding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.email} - {self.quantity} {self.nft.symbol}"


class Transaction(models.Model):
    TYPE = [("BUY", "Buy"), ("SELL", "Sell")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TYPE, default="BUY")
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.transaction_type}{self.quantity} {self.stock.symbol} @ {self.price}"


class UserHolding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.email} - {self.quantity} {self.stock.symbol}"


# Define a model for StockPrice (to store historical price data)
class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user_holdings = GenericRelation(UserHolding)


class News(models.Model):
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    cover_image = models.ImageField(
        upload_to="news_covers/",
        null=True,
        blank=True,
        default="news_covers/placeholder.png",
    )
    description = models.TextField(max_length=1000)
    likes = models.ManyToManyField(User, blank=True, null=True)
    publish_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class NewsComments(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    comment = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CourseCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Topics"


class Learn(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, default=1)
    slug = models.SlugField(default="", null=False)
    image = models.ImageField(
        upload_to="topic_images/",
        null=True,
        blank=True,
        default="topic_images/no-image-available.png",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Subjects"


class Feedback(models.Model):
    topic = models.ForeignKey(Learn, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    feedback = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class GlossaryTerm(models.Model):
    term = models.CharField(max_length=100, unique=True)
    definition = models.TextField()

    def __str__(self):
        return self.term
