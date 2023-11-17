from django import forms
from .models import User, Post, Comment,Transaction,NewsComments, News
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

# from django.contrib.auth.forms import UserCreationForm

from .models import User, Post, Comment, Transaction, NewsComments, Feedback, Stock, CourseCategory


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


class BuyStockForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control'}))
    stripeToken = forms.CharField(widget=forms.HiddenInput())


class SellStockForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control'}))
    stock_symbol = forms.CharField(widget=forms.HiddenInput())


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


class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'cover_image','sub_title', 'description']
        widgets = {
            'cover_image': forms.FileInput(attrs={'class': "news-file-upload-input form-input-field"}),
            'title': forms.TextInput(attrs={'class': "news-title-input form-input-field", 'placeholder': "Enter Title"}),
            'sub_title': forms.TextInput(attrs={'class': "news-sub-title-input form-input-field", 'placeholder': "Enter Sub-Title"}),
            'description': forms.Textarea(attrs={'class': "news-description-input form-input-field", 'placeholder': "Enter News Description"}),
        }
        exclude = ['publish_datetime']

    title = forms.CharField(label="News Title", required=True, max_length=225)
    sub_title = forms.CharField(label="News Sub Title", required=False, max_length=225)
    description = forms.CharField(label="News Description", required=True, max_length=1000, widget=forms.Textarea)
    cover_image = forms.ImageField(label="Cover Image", required=False)

class FeedbackRatingForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["subject", "feedback", "rating"]


class StockFilterForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields=["current_price"]

class CurrencyConverterForm(forms.Form):
    amount = forms.DecimalField(min_value=0.01, label='Amount', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    currency_from = forms.ChoiceField(label='From Currency', widget=forms.Select(attrs={'class': 'form-control'}))
    currency_to = forms.ChoiceField(label='To Currency', widget=forms.Select(attrs={'class': 'form-control'}))

    def set_currency_choices(self, choices):
        self.fields['currency_from'].choices = choices
        self.fields['currency_to'].choices = choices

class TopicCreateForm(forms.ModelForm):
    class Meta:
        model = CourseCategory
        fields = ['name']