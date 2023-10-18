from django.contrib import admin

from .models import User,Stock,StockPrice

# Register your models here.
admin.site.register(User)
admin.site.register(Stock)
admin.site.register(StockPrice)
