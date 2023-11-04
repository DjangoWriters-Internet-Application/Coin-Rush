from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import login

from .forms import RegistrationForm
from .models import (
    Transaction,
    UserHolding,
    User,
    Learn,
    CourseCategory,
    News,
    Post,
    Comment,
)

# from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, "index.html")


# def signup(request):
#     return render(request, "registration/signup.html")


def register(request):
    context = {"form": "", "errors": ""}
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect("home")  # Redirect to the home page after registration

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
    response = HttpResponse()
    for transaction in transactions:
        para = "<p>" + str(transaction) + "</p>"
        response.write(para)
    return response
    # return render(request, 'transaction_history.html', {'transactions': transactions})4


def user_holdings(request):
    user = request.user  # Assuming users are authenticated
    holdings = UserHolding.objects.filter(user=user)
    response = HttpResponse()
    for holding in holdings:
        para = "<p>" + str(holding) + "</p>"
        response.write(para)
    return response
    # return render(request, 'user_holdings.html', {'holdings': holdings})


def categories_course(request):
    categories = CourseCategory.objects.all()
    response = "Categories and Courses:\n" + "<br>"
    for category in categories:
        response += f"\nCategory: {category.name}\n" + "<br>"
        courses = Learn.objects.filter(category=category)
        for course in courses:
            response += (
                "<li>"
                + f"Course: {course.title} - {course.description}\n"
                + "</li><br>"
            )
    return HttpResponse(response)


def discussion(request):
    post_list = Post.objects.all()  # Replace with your queryset for your posts
    paginator = Paginator(post_list, 2)  # Show 5 posts per page
    page = request.GET.get("page")
    posts = paginator.get_page(page)
    return render(request, "posts/discussion_all.html", {"posts": posts})


def discussion_single(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comment_set.all().order_by("-created_at")

    # Add pagination for comments (e.g., 5 comments per page)
    paginator = Paginator(comments, 1)
    page = request.GET.get("page")
    comments_page = paginator.get_page(page)

    return render(
        request,
        "posts/discussion_single.html",
        {"post": post, "comments": comments_page},
    )
