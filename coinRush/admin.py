from django.contrib import admin

<<<<<<< HEAD
from .models import User,Post,Comment,Stock,StockPrice,Transaction,UserHolding, News, NewsComments, Learn, CourseCategory, Feedback

class MemberAdmin(admin.ModelAdmin):
    list_display = ("title", "description",)
    prepopulated_fields = {"slug": ("title",)}
=======
from .models import User,Post,Comment,Stock,StockPrice,Transaction,UserHolding, News, Learn, CourseCategory
>>>>>>> 9683ce4c0d2637669ef27804c14c320e3dbd8461

# Register your models here.
admin.site.register(User)
admin.site.register(Stock)
admin.site.register(StockPrice)
admin.site.register(Transaction)
admin.site.register(UserHolding)
admin.site.register(News)
admin.site.register(Learn, MemberAdmin)
admin.site.register(CourseCategory)
admin.site.register(Feedback)
admin.site.register(Post)
admin.site.register(Comment)
