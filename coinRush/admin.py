from django.contrib import admin

from .models import User,Stock,StockPrice,Transaction,UserHolding, News, Learn, CourseCategory

# Register your models here.
admin.site.register(User)
admin.site.register(Stock)
admin.site.register(StockPrice)
admin.site.register(Transaction)
admin.site.register(UserHolding)
admin.site.register(News)
admin.site.register(Learn)
admin.site.register(CourseCategory)
