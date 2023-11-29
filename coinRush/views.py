from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password, check_password
from decimal import Decimal
import stripe
from .filters import StockFilters
from .constants import top_30_currencies, crypto_data
import requests
import pybase64
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .managers import AuthUserManager

from .forms import (
    BuyNFTForm,
    RegistrationForm,
    PostForm,
    CommentForm,
    NewsCommentForm,
    FeedbackRatingForm,
    BuyStockForm,
    NFTForm,
    CurrencyConverterForm,
    NewsCreateForm,
    TopicCreateForm,
    SubjectCreateForm,
    CustomAuthenticationForm,
    TransactionFilterForm,
    SellStockForm,
    SellNFTForm,
    ProfileImageForm,
    PhotoIdForm,
)

from .models import (
    Transaction,
    UserHolding,
    Learn,
    StockPrice,
    CourseCategory,
    Feedback,
    News,
    Post,
    Stock,
    NFT,
    GlossaryTerm,
    NFTTransaction,
    NFTUserHolding,
    User,
)
import random
import string

stripe.api_key = settings.STRIPE_PRIVATE_KEY


def home(request):
    ord_by = request.GET.get("order_by")
    order_string = ""
    if ord_by == None or ord_by == "max-price" or ord_by == "":
        order_string = "-current_price"
    elif ord_by == "min-price":
        order_string = "current_price"
    elif ord_by == "max-market-cap":
        order_string = "-market_cap"
    elif ord_by == "min-market-cap":
        order_string = "market_cap"
    stocks = Stock.objects.all().order_by(order_string)
    stock_filter = StockFilters(request.GET, queryset=stocks)
    paginator = Paginator(stock_filter.qs, 10)
    page = request.GET.get("page")
    stocks_page = paginator.get_page(page)
    top_10_stocks = Stock.objects.all().order_by("-current_price")[:10]
    trendingNews = News.objects.all().order_by('-likes')[:3]
    trendingDiscussion = Post.objects.all().order_by('-views')[:3]

    context = {
        "stocks": stocks_page,
        "form": stock_filter.form,
        "top_stocks": top_10_stocks,
        "trendingNews": trendingNews,
        "trendingDiscussion": trendingDiscussion,
    }
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


def services(request):
    return render(request, "services.html")


def custom_login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, request.POST)

        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data["username"])

            if check_password(form.data["password"], user.password):
                # Use the login() function to log in the user
                login(request, user)
                # Redirect to a success page or the home page
                return redirect("home")

    else:
        form = CustomAuthenticationForm()

    return render(request, "registration/login.html", {"form": form})


def register(request):
    context = {"form": "", "errors": ""}
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # user = form.save(commit=False)

            # password = form.cleaned_data["password"]
            # hashed_password = make_password(password)
            # user.set_password(hashed_password)

            user = User.objects.create_user(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                name=form.cleaned_data["name"],
            )

            print(user.email, user.password)
            # user.save()

            added_user = User.objects.get(email=user.email)

            if check_password(form.cleaned_data["password"], added_user.password):
                login(request, user)

                # Redirect to the home page after registration
                return redirect("home")

        context["errors"] = form.errors
        context["form"] = form
    else:
        form = RegistrationForm()
        context["form"] = form
    return render(request, "registration/register.html", context)


def generate_reference_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


@login_required(login_url="/login/")
def user_profile(request):
    form = ProfileImageForm()
    photo_id_form = PhotoIdForm()

    user = get_object_or_404(User, pk=request.user.id)
    if user:
        if user.profile_pic is not None:
            binary_data = pybase64.b64decode(user.profile_pic)
            photo_id_binary_data = pybase64.b64decode(user.photo_id)

            # Encode the binary data back to base64 to use in the template
            encoded_image = pybase64.b64encode(binary_data).decode("utf-8")
            photo_id_encoded_image = pybase64.b64encode(photo_id_binary_data).decode(
                "utf-8"
            )
    if request.method == "POST" and "claim_wallet" in request.POST:
        if user.photo_id:
            reference_id = generate_reference_id()
            messages.success(request,
                             f'Your money has been claimed successfully. Please email coinrush@gmail.com with the reference ID {reference_id} to complete the process.\n\nThank you!')
        else:
            # User has not uploaded the photo ID, show a message
            messages.warning(request, "Please upload your photo ID before claiming the money.")

    return render(
        request,
        "registration/user-profile.html",
        {
            "profile_image_form": form,
            "photo_id_form": photo_id_form,
            "encoded_image": encoded_image,
            "photo_id_encoded_image": photo_id_encoded_image,
            "wallet": user.wallet
        },
    )


def upload_image(request, type_id=1):
    if request.method == "POST":
        form = ProfileImageForm(request.POST, request.FILES)

        if form.is_valid():
            user = get_object_or_404(User, pk=request.user.id)
            if request.user.is_authenticated:
                print(type_id)
                if type_id == 1:
                    # case profile_img
                    form_img = form.cleaned_data["profile_img"]

                    b64img_bytes = pybase64.b64encode(form_img.file.read())
                    b64img = b64img_bytes.decode("utf-8")

                    user.profile_pic = b64img

                user.save()
            return redirect("/profile")

    else:
        form = ProfileImageForm()

    return render(request, "registration/user-profile.html", {"form": form})


def upload_photo_image(request, type_id=1):
    if request.method == "POST":
        form = PhotoIdForm(request.POST, request.FILES)

        if form.is_valid():
            user = get_object_or_404(User, pk=request.user.id)
            if request.user.is_authenticated:
                form_img = form.cleaned_data["photo_id"]

                b64img_bytes = pybase64.b64encode(form_img.file.read())
                b64img = b64img_bytes.decode("utf-8")

                user.photo_id = b64img

                user.save()

            return redirect("/profile")

    else:
        form = PhotoIdForm()

    return render(request, "registration/user-profile.html", {"form": form})


def delete_profile_pic(request):
    user = get_object_or_404(User, pk=request.user.id)
    user.profile_pic = ""
    user.save()

    return JsonResponse({"message": "View executed successfully"})


def news(request):
    displayForm = False
    if request.method == "POST":
        if "like_news" in request.POST:
            news_id = request.POST["like_news"]
            news_instance = get_object_or_404(News, pk=news_id)
            request.user.liked_news.add(news_instance)
            news_instance.likes.add(request.user)
        elif "unlike_news" in request.POST:
            news_id = request.POST["unlike_news"]
            news_instance = get_object_or_404(News, pk=news_id)
            request.user.liked_news.remove(news_instance)
            news_instance.likes.remove(request.user)
        elif "title" in request.POST:
            print(request.POST)
            newsCreated = NewsCreateForm(request.POST, request.FILES)
            if newsCreated.is_valid():
                news_instance = newsCreated.save(commit=False)
                news_instance.cover_image.upload_to = (
                    "news_covers/"  # Set the upload_to directory
                )
                news_instance.publish_datetime = timezone.now()
                print(news_instance)
                news_instance.save()
                messages.success(request, "News created successfully!")
                return redirect("news")

    newsForm = NewsCreateForm()
    context = {
        "title": "Latest Crypto News",
        "news": News.objects.all(),
        "newsForm": newsForm,
        "displayForm": displayForm,
    }
    return render(request, "News/index.html", context)


@login_required(login_url="/login/")
def transaction_history(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by("-timestamp")

    if request.method == "GET":
        form = TransactionFilterForm(request.GET)

        if form.is_valid():
            transaction_type = form.cleaned_data.get("transaction_type")
            stock_symbol = form.cleaned_data.get("stock_symbol")
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            if start_date and end_date and start_date > end_date:
                form.add_error(
                    "start_date", "Start date cannot be greater than end date."
                )
            else:
                if transaction_type:
                    transaction_type = transaction_type.capitalize()
                    transactions = transactions.filter(
                        transaction_type=transaction_type
                    )
                if stock_symbol:
                    transactions = transactions.filter(
                        stock__symbol__icontains=stock_symbol
                    )
                if start_date:
                    transactions = transactions.filter(timestamp__gte=start_date)
                if end_date:
                    transactions = transactions.filter(timestamp__lte=end_date)

    items_per_page = 10
    paginator = Paginator(transactions, items_per_page)
    page = request.GET.get("page")

    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)
    form = TransactionFilterForm(request.GET)
    return render(
        request,
        "transaction/transaction_history.html",
        {"transactions": transactions, "form": form},
    )


def categories_course(request):
    categories = CourseCategory.objects.all()
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        form = TopicCreateForm(request.POST)
        if form.is_valid():
            new_topic = form.cleaned_data["name"]
            existing_topic = CourseCategory.objects.filter(name=new_topic).first()
            if existing_topic:
                messages.error(request, f'Topic "{new_topic}" already exists.')
            else:
                form.save()
                messages.success(request, f'Topic "{new_topic}" created successfully.')
            return redirect(url)

        form2 = SubjectCreateForm(request.POST, request.FILES)
        if form2.is_valid():
            learn_instance = form2.save(commit=False)
            learn_instance.image.upload_to = "topic_images/"
            learn_instance.save()
            messages.success(request, "Subject added successfully!")
            return redirect(url)
    else:
        form = TopicCreateForm()
        form2 = SubjectCreateForm()
    return render(
        request,
        "Learn/learning.html",
        {"categories": categories, "form": form, "form2": form2},
    )


def subject_info(request, slug):
    subject = get_object_or_404(Learn, slug=slug)
    description = subject.description
    image = request.FILES.get("image")
    return render(
        request,
        "Learn/learning-details.html",
        {"subject": subject, "description": description, "image": image},
    )


def submit_feedback(request, sub_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            feedbacks = Feedback.objects.get(user__id=request.user.id, topic__id=sub_id)
            form = FeedbackRatingForm(request.POST, instance=feedbacks)
            form.save()
            messages.success(request, "Thank you! Your feedback has been updated.")
            return redirect(url)
        except Feedback.DoesNotExist:
            form = FeedbackRatingForm(request.POST)
            if form.is_valid():
                data = Feedback()
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.feedback = form.cleaned_data["feedback"]
                data.ip = request.META.get("REMOTE_ADDR")  # Change this line
                data.topic_id = sub_id
                data.user_id = request.user.id
                data.save()
                messages.success(
                    request, "Thank you! Your feedback has been submitted."
                )
                return redirect(url)


def discussion(request):
    ord_by = request.GET.get("order_by")
    order_string = "-views"
    if ord_by == None or ord_by == "max-views" or ord_by == "":
        order_string = "-views"
    elif ord_by == "min-views":
        order_string = "views"
    elif ord_by == "latest":
        order_string = "-created_at"
    elif ord_by == "oldest":
        order_string = "created_at"

    post_list = Post.objects.all().order_by(
        order_string
    )
    paginator = Paginator(post_list, 3)  # Show 5 posts per page
    page = request.GET.get("page")
    posts = paginator.get_page(page)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user  # Assign the logged-in user
            post.save()
            return redirect("discussion")
    else:
        form = PostForm()
    return render(request, "posts/discussion_all.html", {"posts": posts, "form": form})


def discussion_single(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comment_set.all().order_by("-created_at")

    paginator = Paginator(comments, 3)
    page = request.GET.get("page")
    comments_page = paginator.get_page(page)

    # Construct a unique session key for the post
    session_key = f"visited_post_{post_id}"

    if not request.session.get(session_key, False):
        # If the session key is not present, increment views and set the session
        post.views += 1
        post.save()
        request.session[session_key] = True

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.created_by = request.user
            comment.save()
            return redirect("discussion_single", post_id=post_id)

    else:
        form = CommentForm()

    return render(
        request,
        "posts/discussion_single.html",
        {"post": post, "comments": comments_page, "form": form},
    )


def stock_chart(request, stock_id):
    stock = Stock.objects.get(pk=stock_id)
    priced_stock = StockPrice.objects.filter(stock=stock).order_by("date")
    dates = [str(stock.date) for stock in priced_stock]
    price = [str(stock.price) for stock in priced_stock]
    return render(request, "stock_prices_chart.html", {"price": price, "dates": dates})


# def newsDetails(request, news_id):
#     news_instance = get_object_or_404(News, pk=news_id)
#     if request.method=='POST':
#         if "like_news" in request.POST:
#             news_id = request.POST["like_news"]
#             request.user.liked_news.add(news_instance)
#             news_instance.likes.add(request.user)
#         elif "unlike_news" in request.POST:
#             news_id = request.POST["unlike_news"]
#             request.user.liked_news.remove(news_instance)
#             news_instance.likes.remove(request.user)
#         news_instance.save()
#     else:
#         userLikedNews=None
#         if request.user.is_authenticated:
#             userLikedNews = request.user.liked_news.all()
#     return render(request, "NewsDetails/index.html", {"news": newsDetails,'userLikedNews':userLikedNews})
#

@login_required(login_url="/login/")
def buy_stock(request, stock_symbol):
    error_message = ""
    stocks = Stock.objects.get(symbol=stock_symbol)
    if request.method == "POST":
        form = BuyStockForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data["quantity"]
            stock = stocks
            total_price = stock.current_price * quantity  # Calculate total price

            # Handle Stripe payment
            token = form.cleaned_data["stripeToken"]
            try:
                charge = stripe.Charge.create(
                    amount=int(total_price * 100),  # Amount in cents
                    currency="cad",
                    source=token,
                    description=f"Stock Purchase: {stock_symbol}",
                )

                # Record the transaction
                transaction = Transaction(
                    user=request.user,
                    stock=stock,
                    transaction_type="Buy",
                    quantity=quantity,
                    price=total_price,
                )
                transaction.save()

                # Update user holdings
                holding, created = UserHolding.objects.get_or_create(
                    user=request.user, stock=stock
                )
                holding.quantity += quantity
                holding.save()

                return redirect("transaction-history")
            except stripe.error.CardError as e:
                error_message = e.error.message
                print(f"Stripe CardError: {error_message}")
    else:
        form = BuyStockForm()

    return render(
        request,
        "Stocks/buy_stock.html",
        {
            "stock": stocks,
            "error_message": error_message,
            "PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            "form": form,
        },
    )


@login_required(login_url="/login/")
def user_holdings(request):
    holdings = UserHolding.objects.filter(user=request.user)
    sell_form = SellStockForm()
    items_per_page = 10
    paginator = Paginator(holdings, items_per_page)
    page = request.GET.get("page")

    try:
        holdings_page = paginator.page(page)
    except PageNotAnInteger:
        holdings_page = paginator.page(1)
    except EmptyPage:
        holdings_page = paginator.page(paginator.num_pages)
    if request.method == "POST":
        sell_form = SellStockForm(request.POST)

        if sell_form.is_valid():
            stock_symbol = sell_form.cleaned_data["stock_symbol"]
            quantity_to_sell = sell_form.cleaned_data["quantity"]
            stock = Stock.objects.get(symbol=stock_symbol)
            holding = holdings.filter(stock=stock).first()
            if (
                    holding
                    and quantity_to_sell > 0
                    and quantity_to_sell <= holding.quantity
            ):
                sell_price = stock.current_price * quantity_to_sell

                sell_transaction = Transaction(
                    user=request.user,
                    stock=stock,
                    transaction_type="Sell",
                    quantity=quantity_to_sell,
                    price=sell_price,
                )
                sell_transaction.save()
                holding.quantity -= quantity_to_sell
                holding.save()
                request.user.wallet += Decimal(sell_price)
                request.user.save()
                if holding.quantity == 0:
                    holding.delete()

                return redirect("user-holdings")
            else:
                error_message = (
                    "Invalid quantity to sell. Please select a valid quantity."
                )
                sell_form.add_error("quantity", error_message)

    return render(
        request,
        "userholding/user_holdings.html",
        {"user": request.user, "holdings": holdings_page, "sell_form": sell_form},
    )


def categories_course(request):
    categories = CourseCategory.objects.all()
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        form = TopicCreateForm(request.POST)
        if form.is_valid():
            new_topic = form.cleaned_data["name"]
            existing_topic = CourseCategory.objects.filter(name=new_topic).first()
            if existing_topic:
                messages.error(request, f'Topic "{new_topic}" already exists.')
            else:
                form.save()
                messages.success(request, f'Topic "{new_topic}" created successfully.')
            return redirect(url)

        form2 = SubjectCreateForm(request.POST, request.FILES)
        if form2.is_valid():
            learn_instance = form2.save(commit=False)
            learn_instance.image.upload_to = "topic_images/"
            learn_instance.save()
            messages.success(request, "Subject added successfully!")
            return redirect(url)
    else:
        form = TopicCreateForm()
        form2 = SubjectCreateForm()
    return render(
        request,
        "Learn/learning.html",
        {"categories": categories, "form": form, "form2": form2},
    )


def subject_info(request, slug):
    subject = get_object_or_404(Learn, slug=slug)
    description = subject.description
    image = request.FILES.get("image")
    return render(
        request,
        "Learn/learning-details.html",
        {"subject": subject, "description": description, "image": image},
    )


def submit_feedback(request, sub_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            feedbacks = Feedback.objects.get(user__id=request.user.id, topic__id=sub_id)
            form = FeedbackRatingForm(request.POST, instance=feedbacks)
            form.save()
            messages.success(request, "Thank you! Your feedback has been updated.")
            return redirect(url)
        except Feedback.DoesNotExist:
            form = FeedbackRatingForm(request.POST)
            if form.is_valid():
                data = Feedback()
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.feedback = form.cleaned_data["feedback"]
                data.ip = request.META.get("REMOTE_ADDR")  # Change this line
                data.topic_id = sub_id
                data.user_id = request.user.id
                data.save()
                messages.success(
                    request, "Thank you! Your feedback has been submitted."
                )
                return redirect(url)


def stock_chart(request, stock_id):
    stock = Stock.objects.get(pk=stock_id)
    priced_stock = StockPrice.objects.filter(stock=stock).order_by("date")
    dates = [str(stock.date) for stock in priced_stock]
    price = [str(stock.price) for stock in priced_stock]
    return render(request, "stock_prices_chart.html", {"price": price, "dates": dates, 'stock': stock})


def newsDetails(request, news_id):
    news_instance = get_object_or_404(News, pk=news_id)
    newsDetails = news_instance
    if request.method == 'POST':
        if "like_news" in request.POST:
            news_id = request.POST["like_news"]
            request.user.liked_news.add(news_instance)
            news_instance.likes.add(request.user)
            news_instance.save()
        elif "unlike_news" in request.POST:
            news_id = request.POST["unlike_news"]
            request.user.liked_news.remove(news_instance)
            news_instance.likes.remove(request.user)
            news_instance.save()
    userLikedNews = None
    if request.user.is_authenticated:
        userLikedNews = request.user.liked_news.all()
    return render(request, "NewsDetails/index.html", {"news": newsDetails, "userLikedNews": userLikedNews})


def nftmarketplace(request):
    nfts = NFT.objects.all()
    return render(request, "Nft/NFTmarketplace.html", {"nfts": nfts})


def nft_detail(request, nft_id):
    nft = get_object_or_404(NFT, pk=nft_id)
    return render(request, "nft/NFT.html", {"nft": nft})

@login_required(login_url="/login/")
def create_nft(request):
    if request.method == "POST":
        form = NFTForm(request.POST, request.FILES)
        if form.is_valid():
            nft_instance = form.save(commit=False)

            # Check if the user is authenticated (logged in)
            if request.user.is_authenticated:
                nft_instance.owner = request.user
                nft_instance.save()
                return redirect("NFTMarketPlace")
            else:
                # Handle the case when the user is not logged in (redirect to login page, for example)
                return redirect("login")  # Replace 'login' with the actual login URL

    else:
        form = NFTForm()

    return render(request, "nft/create_nft.html", {"form": form})



@login_required(login_url="/login/")
def buy_nft(request, nft_symbol):
    error_message = ""
    nft = NFT.objects.get(symbol=nft_symbol)

    if request.method == "POST":
        form = BuyNFTForm(request.POST)

        if form.is_valid():
            quantity_to_buy  = form.cleaned_data["quantity"]
            if quantity_to_buy <= nft.quantity:
                total_price = nft.current_price * quantity_to_buy

                # Handle Stripe payment
                token = form.cleaned_data["stripeToken"]
                try:
                    charge = stripe.Charge.create(
                        amount=int(total_price * 100),  # Amount in cents
                        currency="cad",
                        source=token,
                        description=f"NFT Purchase: {nft_symbol}",
                    )

                    nft_transaction = NFTTransaction(
                        user=request.user,
                        nft=nft,
                        transaction_type="BUY",
                        quantity=quantity_to_buy,
                        price=total_price,
                    )
                    nft_transaction.save()

                    # Update NFT quantity_available
                    nft.quantity -= quantity_to_buy
                    nft.save()

                    # Update user holdings
                    holding, created = NFTUserHolding.objects.get_or_create(
                        user=request.user, nft=nft
                    )
                    holding.quantity += quantity_to_buy
                    holding.save()

                    return redirect("nft-transaction-history")
                except Exception as e:
                    error_message = str(e)
            else:
                error_message = "Not enough NFTs available to fulfill your request."

    else:
        form = BuyNFTForm()

    context = {
        "nft": nft,
        "error_message": error_message,
        "PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
        "form": form,
    }

    return render(request, "nft/buy_nft.html", context)


@login_required(login_url="/login/")
def nft_transaction_history(request):
    user = request.user
    nft_transactions = NFTTransaction.objects.filter(user=user).order_by("-timestamp")
    if request.method == "GET":
        form = TransactionFilterForm(request.GET)
        if form.is_valid():
            transaction_type = form.cleaned_data.get("transaction_type")
            stock_symbol = form.cleaned_data.get("nft_symbol")
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            if start_date and end_date and start_date > end_date:
                form.add_error(
                    "start_date", "Start date cannot be greater than end date."
                )
            else:
                if transaction_type:
                    nft_transactions = nft_transactions.filter(
                        transaction_type=transaction_type
                    )
                if stock_symbol:
                    nft_transactions = nft_transactions.filter(
                        nft__symbol__icontains=stock_symbol
                    )
                if start_date:
                    nft_transactions = nft_transactions.filter(
                        timestamp__gte=start_date
                    )
                if end_date:
                    nft_transactions = nft_transactions.filter(timestamp__lte=end_date)

    items_per_page = 10
    paginator = Paginator(nft_transactions, items_per_page)
    page = request.GET.get("page")

    try:
        nft_transactions = paginator.page(page)
    except PageNotAnInteger:
        nft_transactions = paginator.page(1)
    except EmptyPage:
        nft_transactions = paginator.page(paginator.num_pages)
    form = TransactionFilterForm(request.GET)
    return render(
        request,
        "transaction/nft_transaction_history.html",
        {"nft_transactions": nft_transactions, "form": form},
    )


@login_required(login_url="/login/")
def nft_user_holdings(request):
    holdings = NFTUserHolding.objects.filter(user=request.user)
    sell_form = SellNFTForm()
    items_per_page = 10
    paginator = Paginator(holdings, items_per_page)
    page = request.GET.get("page")

    try:
        holdings_page = paginator.page(page)
    except PageNotAnInteger:
        holdings_page = paginator.page(1)
    except EmptyPage:
        holdings_page = paginator.page(paginator.num_pages)

    if request.method == "POST":
        sell_form = SellNFTForm(request.POST)

        if sell_form.is_valid():
            nft_symbol = sell_form.cleaned_data["nft_symbol"]
            quantity_to_sell = sell_form.cleaned_data["quantity"]
            nft = NFT.objects.get(symbol=nft_symbol)
            holding = holdings.filter(nft=nft).first()

            if (
                    holding
                    and quantity_to_sell > 0
                    and quantity_to_sell <= holding.quantity
            ):
                sell_price = nft.current_price * quantity_to_sell

                sell_transaction = NFTTransaction(
                    user=request.user,
                    nft=nft,
                    transaction_type="SELL",
                    quantity=quantity_to_sell,
                    price=sell_price,
                )
                sell_transaction.save()

                holding.quantity -= quantity_to_sell
                holding.save()

                request.user.wallet += Decimal(sell_price)
                request.user.save()

                if holding.quantity == 0:
                    holding.delete()

                return redirect("nft-user-holdings")
            else:
                error_message = (
                    "Invalid quantity to sell. Please select a valid quantity."
                )
                sell_form.add_error("quantity", error_message)

    return render(
        request,
        "userholding/nft_user_holdings.html",
        {"user": request.user, "holdings": holdings_page, "sell_form": sell_form},
    )


def convert(source, to, amount):
    # Corrected dictionary creation with ID as key and name as value
    collective_dict = {str(identifier): name for identifier, name in top_30_currencies}
    collective_dict.update({str(identifier): name for identifier, name in crypto_data})

    # collective_dict += {name: identifier for identifier, name in crypto_data}

    # url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    # url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/map'
    url = "https://pro-api.coinmarketcap.com/v2/tools/price-conversion"

    # url = 'https://sandbox-api.coinmarketcap.com/v2/tools/price-conversion'
    parameters = {"id": source, "convert_id": to, "amount": amount}

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "6f66fcc3-73b3-48ea-a584-32af97de8e12",
        # "X-CMC_PRO_API_KEY": "b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c",
    }

    try:
        response = requests.get(url, params=parameters, headers=headers)
        data = response.json()
        # return str(amount) + " " + collective_dict[str(source)] + " = " + str(
        #     round(data['data'][source]['quote'][to]['price'], 4)) + " " + collective_dict[str(to)]
        return (
                str(amount)
                + " "
                + collective_dict[str(source)]
                + " = "
                + str(round(data["data"]["quote"][to]["price"], 4))
                + " "
                + collective_dict[str(to)]
        )
    except:
        return "Some error occured"


def convert_data(request):
    result = None

    # Example choices (you can replace this with actual currency choices)
    currency_choices = top_30_currencies + crypto_data
    currency_choices = top_30_currencies + crypto_data

    if request.method == "POST":
        form = CurrencyConverterForm(request.POST)
        form.set_currency_choices(currency_choices)
        if form.is_valid():
            result = convert(
                form.cleaned_data["currency_from"],
                form.cleaned_data["currency_to"],
                form.cleaned_data["amount"],
            )
        return render(
            request, "converter_template.html", {"form": form, "result": result}
        )

    else:
        form = CurrencyConverterForm()
        form.set_currency_choices(currency_choices)

    return render(request, "converter_template.html", {"form": form, "result": result})


def glossary(request):
    # Retrieve all glossary terms ordered alphabetically
    terms = GlossaryTerm.objects.order_by("term")

    return render(request, "Glossary/Terms.html", {"terms": terms})


def term_detail(request, term_id):
    # Retrieve the detailed information for a specific term
    term = get_object_or_404(GlossaryTerm, id=term_id)

    return render(request, "Glossary/Terms_details.html", {"term": term})
