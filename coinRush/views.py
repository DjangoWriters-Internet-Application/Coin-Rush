from django.shortcuts import render
from django.http import HttpResponse
from .models import Transaction,UserHolding, User, Learn, CourseCategory, News

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


def news(request):
    context = {
        'title': "Latest Crypto News",
        'news':  News.objects.all()
    }
    return render(request, "News/index.html", context)


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

def categories_course(request):
    categories = CourseCategory.objects.all()
    response = "Categories and Courses:\n" + '<br>'
    for category in categories:
        response += f"\nCategory: {category.name}\n" + '<br>'
        courses = Learn.objects.filter(category=category)
        for course in courses:
            response += '<li>' + f"Course: {course.title} - {course.description}\n" + '</li><br>'
    return HttpResponse(response)


