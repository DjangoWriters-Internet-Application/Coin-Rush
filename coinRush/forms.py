from django import forms
from .models import User, Post, Comment
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