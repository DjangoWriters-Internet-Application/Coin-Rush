from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", lambda request: redirect("login/"), name="redirect_to_login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("register/", views.register, name="register"),
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("news/", views.news, name="news"),
    path("news/<int:news_id>", views.newsDetails, name="news_details"),
    path("transaction-history/", views.transaction_history, name="transaction-history"),
    path("user-holdings/", views.user_holdings, name="user-holdings"),
    path("learn/", views.categories_course, name="courses"),
    path("learn/<slug:slug>/", views.subject_info, name="subject_info"),
    path("submit_feedback/<int:sub_id>/", views.submit_feedback, name="submit_feedback"),
    path("discussion/", views.discussion, name="discussion"),
    path("discussion/<int:post_id>", views.discussion_single, name="discussion_single"),
    path("show_stocks/", views.show_stocks, name="show_stocks"),
    path("buy-stock/<str:stock_symbol>/", views.buy_stock, name="buy_stock"),
    path("nft/", views.nftmarketplace, name="NFTMarketPlace"),
    path("nft/<int:nft_id>/", views.nft_detail, name="nft_detail"),
    path('converter/', views.convert_data, name='cryptocurrency_data'),
    path('stock/<int:stock_id>', views.test, name='test'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)