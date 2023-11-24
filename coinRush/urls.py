from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", lambda request: redirect("login/"), name="redirect_to_login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("login/", views.custom_login_view, name="login"),
    path("register/", views.register, name="register"),
    path("profile/", views.user_profile, name="user-profile"),
    path("upload-image/", views.upload_image, name="upload-image"),
    path("upload-photo-image/", views.upload_photo_image, name="upload-photo-image"),
    path("delete-profile-pic/", views.delete_profile_pic, name="delete-profile-pic"),
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("news/", views.news, name="news"),
    path("news/<int:news_id>", views.newsDetails, name="news_details"),
    path("transaction-history/", views.transaction_history, name="transaction-history"),
    path("user-holdings/", views.user_holdings, name="user-holdings"),
    path("learn/", views.categories_course, name="courses"),
    path("learn/<slug:slug>/", views.subject_info, name="subject_info"),
    path(
        "submit_feedback/<int:sub_id>/", views.submit_feedback, name="submit_feedback"
    ),
    path("discussion/", views.discussion, name="discussion"),
    path("discussion/<int:post_id>", views.discussion_single, name="discussion_single"),
    path("buy-stock/<str:stock_symbol>/", views.buy_stock, name="buy_stock"),
    path("nft/", views.nftmarketplace, name="NFTMarketPlace"),
    path("nft/<int:nft_id>/", views.nft_detail, name="nft_detail"),
    path("create_nft/", views.create_nft, name="create_nft"),
    path("buy_nft/<str:nft_symbol>/", views.buy_nft, name="buy_nft"),
    path("nft-user-holdings/", views.nft_user_holdings, name="nft-user-holdings"),
    path(
        "nft-transaction-history/",
        views.nft_transaction_history,
        name="nft-transaction-history",
    ),
    path("test/", views.convert_data, name="cryptocurrency_data"),
    path("glossary/", views.glossary, name="glossary"),
    path("glossary/<int:term_id>/", views.term_detail, name="term_detail"),
    path("converter/", views.convert_data, name="cryptocurrency_data"),
    path("stock/<int:stock_id>", views.stock_chart, name="stock_chart"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
