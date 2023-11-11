from django import forms
from django.contrib.auth.forms import AuthenticationForm

# from django.contrib.auth.forms import UserCreationForm

from .models import User, Post, Comment, Transaction, NewsComments


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User

    username = forms.CharField(
        label="USERNAME",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label_suffix="",
    )
    password = forms.CharField(
        label="PASSWORD",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label_suffix="",
    )

    error_messages = {
        "invalid_login": (
            "Please enter a correct username and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": ("This account is inactive."),
    }


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "email", "profile_pic", "is_superuser"]

    name = forms.CharField(
        label="NAME",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label_suffix="",
    )

    password = forms.CharField(
        label="PASSWORD",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label_suffix="",
    )

    email = forms.EmailField(
        label="EMAIL",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label_suffix="",
    )

    is_superuser = forms.BooleanField(
        label="IS_SUPERUSER",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label_suffix="",
    )

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields["profile_pic"].required = False
        self.fields["is_superuser"].required = False
        self.fields["is_superuser"].initial = False


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "topicTitle",
                    "placeholder": "Topic Title",
                    "required": "true",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "id": "topicContent",
                    "rows": "4",
                    "placeholder": "Topic Content",
                    "required": "true",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "id": "add-comment",
                    "rows": "2",
                    "placeholder": "Add Comment...",
                    "required": "true",
                }
            ),
        }


class BuyStockForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["quantity"]

    widgets = {
        "quantity": forms.NumberInput(attrs={"required": "required", "min": "1"}),
    }


class PaymentForm(forms.Form):
    # Include the fields necessary for Stripe payment
    stripeToken = forms.CharField(widget=forms.HiddenInput())


class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComments
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "id": "news-comment-text",
                    "rows": "2",
                    "placeholder": "Add Comment...",
                    "required": "true",
                }
            )
        }


class FeedbackRatingForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["subject", "feedback", "rating"]
