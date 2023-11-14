from django import forms
from .models import User, Post, Comment,Transaction,NewsComments, News
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "email", "profile_pic", "is_superuser"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'topicTitle', 'placeholder': 'Topic Title', 'required': 'true'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'id': 'topicContent', 'rows': '4', 'placeholder': 'Topic Content',
                       'required': 'true'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content']

        widgets= {
            'content':forms.Textarea(
            attrs={'class':'form-control','id':'add-comment','rows':'2','placeholder': 'Add Comment...', 'required': 'true'}
        ),}

class BuyStockForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['quantity']

    widgets = {
        'quantity': forms.NumberInput(attrs={'required': 'required', 'min': '1'}),
    }

class PaymentForm(forms.Form):
    # Include the fields necessary for Stripe payment
    stripeToken = forms.CharField(widget=forms.HiddenInput())


class NewsCommentForm(forms.ModelForm):
    class Meta:
        model=NewsComments
        fields=['comment']
        widgets={
            'comment': forms.Textarea(attrs={'id':'news-comment-text','rows':'2','placeholder': 'Add Comment...', 'required': 'true'})
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
