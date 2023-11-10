from django.contrib import admin

from .models import User,Post,Comment,Stock,StockPrice,Transaction,UserHolding, News, NewsComments, Learn, CourseCategory

class MemberAdmin(admin.ModelAdmin):
    list_display = ("title", "description",)
    prepopulated_fields = {"slug": ("title",)}

# Register your models here.
admin.site.register(User)
admin.site.register(Stock)
admin.site.register(StockPrice)
admin.site.register(Transaction)
admin.site.register(UserHolding)
admin.site.register(News)
admin.site.register(Learn, MemberAdmin)
admin.site.register(CourseCategory)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(NewsComments)
