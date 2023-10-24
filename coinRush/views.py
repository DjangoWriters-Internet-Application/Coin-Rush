from django.shortcuts import render
from django.http import HttpResponse
from .models import Transaction,UserHolding,User
# from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, "index.html")


def signup(request):
    return render(request, "registration/signup.html")


def login(request):
    return render(request, "registration/login.html")


def logout(request):
    return render(request, "index.html")

def transaction_history(request):
    user = request.user  # Assuming users are authenticated
    transactions = Transaction.objects.filter(user=user).order_by('-timestamp')
    response = HttpResponse()
    for transaction in transactions:
        para = '<p>' + str(transaction) + '</p>'
        response.write(para)
    return response
    # return render(request, 'transaction_history.html', {'transactions': transactions})4

def user_holdings(request):
    user = request.user  # Assuming users are authenticated
    holdings = UserHolding.objects.filter(user=user)
    response=HttpResponse()
    for holding in holdings:
        para='<p>'+str(holding)+'</p>'
        response.write(para)
    return response
    # return render(request, 'user_holdings.html', {'holdings': holdings})