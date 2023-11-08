from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("", lambda request: redirect(
        "accounts/login/"), name="redirect_to_login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("roadmap/", views.roadmap, name="roadmap"),
    path("news/", views.news, name="news"),
    path("news/<int:news_id>", views.newsDetails, name="news_details"),
    path("transaction-history/", views.transaction_history, name="transaction-history"),
    path("user-holdings/", views.user_holdings, name="user-holdings"),
    path("courses/", views.categories_course, name="categories_course"),
    path("discussion/", views.discussion, name="discussion"),
    path("discussion/<int:post_id>",
         views.discussion_single, name="discussion_single"),
    path("show_stocks/", views.show_stocks, name="show_stocks"),
    path('buy-stock/', views.buy_stock, name='buy_stock'),
]
