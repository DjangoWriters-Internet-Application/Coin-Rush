from django.contrib import admin
from .models import User,Post,Comment,Stock,StockPrice,Transaction,UserHolding, News, Learn, CourseCategory, Feedback, NFT, Bid, nftTransaction, Purchase

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
admin.site.register(Feedback)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(NFT)
admin.site.register(nftTransaction)
admin.site.register(Purchase)
admin.site.register(Bid)
