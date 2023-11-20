from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import login
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import stripe
from decimal import Decimal
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import *
from .filters import StockFilters
from .constants import top_30_currencies,crypto_data
import requests

from .forms import (
    RegistrationForm,
    PostForm,
    CommentForm,
    NewsCommentForm,
    FeedbackRatingForm,
    BuyStockForm,
    SellStockForm,
    StockFilterForm,
    CurrencyConverterForm,
    NewsCreateForm,
    TopicCreateForm,
    SubjectCreateForm
)

from .forms import (
    CustomAuthenticationForm,
    RegistrationForm,
    PostForm,
    CommentForm,
    NewsCommentForm,
)
from .models import (
    Transaction,
    UserHolding,
    User,
    Learn,
StockPrice,
    CourseCategory,
    Feedback,
    News,
    Post,
    Comment,
    Stock,
    NFT,
    Bid,
)

stripe.api_key = settings.STRIPE_PRIVATE_KEY


# Create your views here.


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

    stock_filter = StockFilters(request.GET,queryset=Stock.objects.all().order_by(order_string))
    top_10_stocks = Stock.objects.all().order_by('-current_price')[:10]

    context = {"stocks": stock_filter.qs,
               "form":stock_filter.form,
               "top_stocks":top_10_stocks}
    return render(request, "index.html",context )

def about(request):
    return render(request, "about.html")



def services(request):
    return render(request, "services.html")


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "registration/login.html"


def register(request):
    context = {"form": "", "errors": ""}
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            hashed_password = make_password(cleaned_data["password"])
            cleaned_data["password"] = hashed_password
            form.cleaned_data = cleaned_data
            user = form.save()
            login(request, user)

            # Redirect to the home page after registration
            return redirect("home")

        context["errors"] = form.errors
        context["form"] = form
    else:
        form = RegistrationForm()
        context["form"] = form
    return render(request, "registration/register.html", context)


def news(request):
    displayForm = False
    if request.method == 'POST':
        if 'like_news' in request.POST:
            news_id = request.POST['like_news']
            news_instance = get_object_or_404(News, pk=news_id)
            request.user.liked_news.add(news_instance)
            news_instance.likes.add(request.user)
        elif 'unlike_news' in request.POST:
            news_id = request.POST['unlike_news']
            news_instance = get_object_or_404(News, pk=news_id)
            request.user.liked_news.remove(news_instance)
            news_instance.likes.remove(request.user)
        elif 'title' in request.POST:
            print(request.POST)
            newsCreated = NewsCreateForm(request.POST, request.FILES)
            if newsCreated.is_valid():
                news_instance = newsCreated.save(commit=False)
                news_instance.cover_image.upload_to = 'news_covers/'  # Set the upload_to directory
                news_instance.publish_datetime = timezone.now()
                print(news_instance)
                news_instance.save()
                messages.success(request, 'News created successfully!')
                return redirect('news')

    newsForm = NewsCreateForm();
    context = {"title": "Latest Crypto News", "news": News.objects.all(), 'newsForm': newsForm, 'displayForm':displayForm}
    return render(request, "News/index.html", context)


@login_required(login_url="/login/")
def transaction_history(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by("-timestamp")

    items_per_page = 10
    paginator = Paginator(transactions, items_per_page)
    page = request.GET.get('page')

    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    return render(
        request, "transaction/transaction_history.html", {
            "transactions": transactions}
    )


def categories_course(request):
    categories = CourseCategory.objects.all()
    url = request.META.get("HTTP_REFERER")
    if request.method == 'POST':
        form = TopicCreateForm(request.POST)
        if form.is_valid():
            new_topic = form.cleaned_data['name']
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
            learn_instance.image.upload_to = 'topic_images/'
            learn_instance.save()
            messages.success(request, 'Subject added successfully!')
            return redirect(url)
    else:
        form = TopicCreateForm()
        form2 = SubjectCreateForm()
    return render(request, "Learn/learning.html", {"categories": categories, 'form': form, 'form2': form2})


def subject_info(request, slug):
    subject = get_object_or_404(Learn, slug=slug)
    description = subject.description
    image = request.FILES.get('image')
    return render(
        request,
        "Learn/learning-details.html",
        {"subject": subject, "description": description, "image": image},
    )


def submit_feedback(request, sub_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            feedbacks = Feedback.objects.get(
                user__id=request.user.id, topic__id=sub_id)
            form = FeedbackRatingForm(request.POST, instance=feedbacks)
            form.save()
            messages.success(
                request, "Thank you! Your feedback has been updated.")
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
    )  # Replace with your queryset for your posts
    paginator = Paginator(post_list, 2)  # Show 5 posts per page
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

    # Add pagination for comments (e.g., 5 comments per page)
    paginator = Paginator(comments, 1)
    page = request.GET.get("page")
    comments_page = paginator.get_page(page)

    # Construct a unique session key for the post
    session_key = f'visited_post_{post_id}'

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


def stock_chart(request,stock_id):
    stock=Stock.objects.get(pk=stock_id)
    priced_stock=StockPrice.objects.filter(stock=stock).order_by('date')
    dates = [str(stock.date) for stock in priced_stock]
    price = [str(stock.price) for stock in priced_stock]
    return render(request, "stock_prices_chart.html",{"price":price,"dates":dates})

def newsDetails(request, news_id):
    if 'like_news' in request.POST:
        news_id = request.POST['like_news']
        news_instance = get_object_or_404(News, pk=news_id)
        request.user.liked_news.add(news_instance)
        news_instance.likes.add(request.user)
    elif 'unlike_news' in request.POST:
        news_id = request.POST['unlike_news']
        news_instance = get_object_or_404(News, pk=news_id)
        request.user.liked_news.remove(news_instance)
        news_instance.likes.remove(request.user)

    newsDetails = get_object_or_404(News, pk=news_id)
    form = NewsCommentForm()
    return render(request, 'NewsDetails/index.html', {'news': newsDetails})

@login_required(login_url="/login/")
def buy_stock(request, stock_symbol):
    error_message = ""
    stocks = Stock.objects.get(symbol=stock_symbol)
    if request.method == 'POST':
        form = BuyStockForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
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
    page = request.GET.get('page')

    try:
        holdings_page = paginator.page(page)
    except PageNotAnInteger:
        holdings_page = paginator.page(1)
    except EmptyPage:
        holdings_page = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        sell_form = SellStockForm(request.POST)

        if sell_form.is_valid():
            stock_symbol = sell_form.cleaned_data['stock_symbol']
            quantity_to_sell = sell_form.cleaned_data['quantity']
            stock = Stock.objects.get(symbol=stock_symbol)
            holding = holdings.filter(stock=stock).first()
            if holding and quantity_to_sell > 0 and quantity_to_sell <= holding.quantity:
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
                error_message = 'Invalid quantity to sell. Please select a valid quantity.'
                sell_form.add_error('quantity', error_message)

    return render(request, 'userholding/user_holdings.html',
                  {'user': request.user, 'holdings': holdings_page, 'sell_form': sell_form})


def newsDetails(request, news_id):
    if request.method == "POST":
        comment = NewsCommentForm(request.POST)

    newsDetails = get_object_or_404(News, pk=news_id)
    form = NewsCommentForm()
    return render(
        request, "NewsDetails/index.html", {"news": newsDetails, "form": form}
    )


def nftmarketplace(request):
    nfts = NFT.objects.all()
    return render(request, "Nft/NFTmarketplace.html", {"nfts": nfts})


def nft_detail(request, nft_id):
    nft = get_object_or_404(NFT, pk=nft_id)
    return render(request, "nft/NFT.html", {"nft": nft})



def convert(source,to,amount):
    # Corrected dictionary creation with ID as key and name as value
    collective_dict = {str(identifier): name for identifier, name in top_30_currencies}
    collective_dict.update({str(identifier): name for identifier, name in crypto_data})

    # collective_dict += {name: identifier for identifier, name in crypto_data}

    # url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    # url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/map'
    # url = 'https://pro-api.coinmarketcap.com/v2/tools/price-conversion'

    url = 'https://sandbox-api.coinmarketcap.com/v2/tools/price-conversion'
    parameters = {
        'id':source,
        'convert_id':to,
        'amount':amount
    }

    headers = {
        "Accepts": "application/json",
        # 'X-CMC_PRO_API_KEY': '6f66fcc3-73b3-48ea-a584-32af97de8e12',
        "X-CMC_PRO_API_KEY": "b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c",
    }

    try:
        response = requests.get(url, params=parameters, headers=headers)
        data=response.json()
        return str(amount) + " "+ collective_dict[str(source)]+" = " + str(round(data['data'][source]['quote'][to]['price'],4))+" "+collective_dict[str(to)]
        # return str(amount) + " "+ collective_dict[str(source)]+" = " + str(round(data['data']['quote'][to]['price'],4))+" "+collective_dict[str(to)]
    except:
        return "Some error occured"

def convert_data(request):
    result = None

    # Example choices (you can replace this with actual currency choices)
    currency_choices = top_30_currencies+crypto_data

    if request.method == 'POST':
        form = CurrencyConverterForm(request.POST)
        form.set_currency_choices(currency_choices)
        if form.is_valid():
            result=convert(form.cleaned_data['currency_from'],form.cleaned_data['currency_to'],form.cleaned_data['amount'])
        return render(request, 'converter_template.html', {'form': form, 'result': result})


    else:
        form = CurrencyConverterForm()
        form.set_currency_choices(currency_choices)

    return render(request, 'converter_template.html', {'form': form, 'result': result})
