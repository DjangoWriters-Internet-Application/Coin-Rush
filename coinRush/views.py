from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import login
from django.conf import settings
import stripe

from .forms import RegistrationForm, PostForm, CommentForm
from .models import (
    Transaction,
    UserHolding,
    User,
    Learn,
    CourseCategory,
    News,
    Post,
    Comment,
    Stock,
)

# from django.contrib.auth.decorators import login_required
stripe.api_key = settings.STRIPE_PRIVATE_KEY

# Create your views here.


def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def services(request):
    return render(request, "services.html")


def register(request):
    context = {"form": "", "errors": ""}
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
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


# def login(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             print("hello")

#         return render(request, "home/", {"form": form})

#     else:
#         form = LoginForm()
#         return render(request, "registration/login.html", {"form": form})


def news(request):
    context = {"title": "Latest Crypto News", "news": News.objects.all()}
    return render(request, "News/index.html", context)


def transaction_history(request):
    user = request.user  # Assuming users are authenticated
    transactions = Transaction.objects.filter(user=user).order_by("-timestamp")
    return render(request, "transaction/transaction_history.html", { "transactions": transactions})


def user_holdings(request):
    user = request.user  # Assuming users are authenticated
    holdings = UserHolding.objects.filter(user=user)
    return render(request, "userholding/user_holdings.html", {"holdings": holdings, "user": user})


def categories_course(request):
    categories = CourseCategory.objects.all()
    return render(request, "Learn/learning.html", {"categories": categories})


def discussion(request):
    post_list = Post.objects.all().order_by(
        "-created_at"
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


def show_stocks(request):
    stocks = Stock.objects.all()
    return render(request, "Stocks/showStocks.html", {"stocks": stocks})


def buy_stock(request,stock_symbol):
    error_message = ''
    if request.method == 'POST':
        # stock_symbol = request.POST.get('stock_symbol')
        print(f"Received stock symbol: {stock_symbol}")
        quantity = int(request.POST.get('quantity', 0))
        if quantity <= 0:
            raise ValueError("Quantity should be a positive integer.")

        stock = Stock.objects.get(symbol=stock_symbol)
        total_price = stock.current_price * quantity  # Calculate total price

        # Handle Stripe payment
        token = request.POST['stripeToken']
        try:
            charge = stripe.Charge.create(
                amount=int(total_price * 100),  # Amount in cents
                currency='cad',
                source=token,
                description=f"Stock Purchase: {stock_symbol}",
            )

            # Record the transaction
            transaction = Transaction(
                user=request.user, stock=stock, transaction_type='Buy', quantity=quantity, price=total_price)
            transaction.save()

            # Update user holdings
            holding, created = UserHolding.objects.get_or_create(
                user=request.user, stock=stock)
            holding.quantity += quantity
            holding.save()
            print(holding)
            return redirect('transaction-history')
        except stripe.error.CardError as e:
            error_message = e.error.message
            print(f"Stripe CardError: {error_message}")

    stocks = Stock.objects.get(symbol=stock_symbol)
    return render(request, 'Stocks/buy_stock.html', {'stock': stocks, 'error_message': error_message, 'PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})
