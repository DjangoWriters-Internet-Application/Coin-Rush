from django.contrib import admin

<<<<<<< HEAD
from .models import User,Stock,StockPrice,Transaction,UserHolding, News, Learn, NFT, Bid
=======
from .models import User,Post,Comment,Stock,StockPrice,Transaction,UserHolding, News, Learn, CourseCategory
>>>>>>> 812fa8e5760b661cb1df79fc4594b139890e311f

# Register your models here.
admin.site.register(User)
admin.site.register(Stock)
admin.site.register(StockPrice)
admin.site.register(Transaction)
admin.site.register(UserHolding)
admin.site.register(News)
admin.site.register(Learn)
<<<<<<< HEAD
admin.site.register(NFT)
admin.site.register(Bid)
=======
admin.site.register(CourseCategory)
admin.site.register(Post)
admin.site.register(Comment)
>>>>>>> 812fa8e5760b661cb1df79fc4594b139890e311f
