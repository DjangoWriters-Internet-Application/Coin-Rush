from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

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
