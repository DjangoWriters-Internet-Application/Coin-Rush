from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path("", views.home, name="home"),
    # path("accounts/", include("coinRush.urls")),
    # path("signup", views.signup, name="signup"),
    # path("login", views.login, name="login"),
    path("", views.home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("news/", views.news, name='news'),
    path("transaction-history/", views.transaction_history, name='transaction-history'),
    path("user-holdings/", views.user_holdings, name='user-holdings'),
    path("courses/", views.categories_course, name='categories_course'),
    path("discussion/", views.discussion, name='discussion'),
    path('buy-stock/', views.buy_stock, name='buy_stock'),
    path("discussion/<int:post_id>", views.discussion_single, name='discussion_single')

]
