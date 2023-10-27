from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator

from .models import Transaction,UserHolding, User, Learn, CourseCategory, News,Post,Comment

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
    return render(request, 'transaction/transaction_history.html', {'transactions': transactions})

def user_holdings(request):
    user = request.user  # Assuming users are authenticated
    holdings = UserHolding.objects.filter(user=user)
    return render(request, 'userholding/user_holdings.html', {'holdings': holdings,'user':user})

def categories_course(request):
    categories = CourseCategory.objects.all()
    response = "Categories and Courses:\n" + '<br>'
    for category in categories:
        response += f"\nCategory: {category.name}\n" + '<br>'
        courses = Learn.objects.filter(category=category)
        for course in courses:
            response += '<li>' + f"Course: {course.title} - {course.description}\n" + '</li><br>'
    return HttpResponse(response)



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