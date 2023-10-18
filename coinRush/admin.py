from django.contrib import admin

from .models import User,Stock,StockPrice,Transaction,UserHolding

# Register your models here.
admin.site.register(User)
admin.site.register(Stock)
admin.site.register(StockPrice)
admin.site.register(Transaction)
admin.site.register(UserHolding)
