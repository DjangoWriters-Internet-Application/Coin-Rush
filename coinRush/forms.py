from django import forms
<<<<<<< HEAD
from .models import User, Post, Comment, NewsComments, Feedback
=======
from .models import User, Post, Comment,Transaction
>>>>>>> 9683ce4c0d2637669ef27804c14c320e3dbd8461
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
<<<<<<< HEAD
        model=NewsComments
        fields=['comment']
        widgets={
            'comment': forms.Textarea(attrs={'id':'news-comment-text','rows':'2','placeholder': 'Add Comment...', 'required': 'true'})
        }

class FeedbackRatingForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'feedback', 'rating']
=======
        model = Transaction
        fields = ['quantity']

    widgets = {
        'quantity': forms.NumberInput(attrs={'required': 'required', 'min': '1'}),
    }

class PaymentForm(forms.Form):
    # Include the fields necessary for Stripe payment
    stripeToken = forms.CharField(widget=forms.HiddenInput())
>>>>>>> 9683ce4c0d2637669ef27804c14c320e3dbd8461
