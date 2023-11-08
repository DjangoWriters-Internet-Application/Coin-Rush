from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.conf import settings
import stripe

from .models import Transaction,UserHolding, User, Learn, CourseCategory, News,Post,Comment,Stock

# from django.contrib.auth.decorators import login_required
stripe.api_key=settings.STRIPE_PRIVATE_KEY
# Create your views here.
def home(request):
    return render(request, "index.html")


def signup(request):
    return render(request, "registration/signup.html")


def login(request):
    return render(request, "registration/login.html")


def logout(request):
    return render(request, "index.html")


def news(request):
    context = {
        'title': "Latest Crypto News",
        'news':  News.objects.all()
    }
    return render(request, "News/index.html", context)


def transaction_history(request):
    user = request.user  # Assuming users are authenticated
    transactions = Transaction.objects.filter(user=user).order_by('-timestamp')
    return render(request, 'transaction/transaction_history.html', {'transactions': transactions})

def user_holdings(request):
    user = request.user  # Assuming users are authenticated
    holdings = UserHolding.objects.filter(user=user)
    return render(request, 'userholding/user_holdings.html', {'holdings': holdings,'user':user})

def categories_course(request):
    categories = CourseCategory.objects.all()
    return render(request, 'Learn/learning.html', {'categories': categories})

def discussion(request):
    post_list = Post.objects.all()  # Replace with your queryset for your posts
    paginator = Paginator(post_list, 2)  # Show 5 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'posts/discussion_all.html', {'posts': posts})


def discussion_single(request,post_id):

    post = get_object_or_404(Post, pk=post_id)
    comments = post.comment_set.all().order_by('-created_at')

    # Add pagination for comments (e.g., 5 comments per page)
    paginator = Paginator(comments, 1)
    page = request.GET.get('page')
    comments_page = paginator.get_page(page)

    return render(request, 'posts/discussion_single.html', {'post': post, 'comments': comments_page})

def buy_stock(request):
    error_message = ''
    if request.method == 'POST':
        stock_symbol = request.POST.get('stock_symbol')
        print(f"Received stock symbol: {stock_symbol}")
        quantity = int(request.POST['quantity'])
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
            transaction = Transaction(user=request.user, stock=stock, transaction_type='Buy', quantity=quantity, price=total_price)
            transaction.save()

            # Update user holdings
            holding, created = UserHolding.objects.get_or_create(user=request.user, stock=stock)
            holding.quantity += quantity
            holding.save()
            print(holding)
            return redirect('transaction-history')
        except stripe.error.CardError as e:
            error_message = e.error.message
            print(f"Stripe CardError: {error_message}")

    stocks = Stock.objects.all()
    return render(request, 'buy_stock.html', {'stocks': stocks, 'error_message': error_message,'PUBLIC_KEY':settings.STRIPE_PUBLIC_KEY})
