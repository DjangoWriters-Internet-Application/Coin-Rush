from django import forms
from .models import User, Post, Comment, Transaction, NewsComments, News
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.text import slugify

# from django.contrib.auth.forms import UserCreationForm

from .models import (
    User,
    Post,
    Comment,
    Transaction,
    NewsComments,
    Feedback,
    Stock,
    CourseCategory,
    Learn,
    GlossaryTerm,
    NFT,
)


from django import forms
from .models import NFTTransaction


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
        fields = ["email", "password"]

    username = forms.CharField(
        label="EMAIL",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label_suffix="",
    )
    password = forms.CharField(
        label="PASSWORD",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label_suffix="",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "EMAIL"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "PASSWORD"}
        )


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        label="EMAIL",
        max_length=255,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "EMAIL"}
        ),
    )
    password = forms.CharField(
        label="PASSWORD",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "PASSWORD"}
        ),
        label_suffix="",
    )

    def __init__(self, *args, **kwargs):
        super(ForgetPasswordForm, self).__init__(*args, **kwargs)
        self.fields["password"].required = False


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "email", "password"]
        # "is_superuser"

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

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")

        return password


class ProfileImageForm(forms.Form):
    profile_img = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )


class PhotoIdForm(forms.Form):
    photo_id = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )


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
    quantity = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    stripeToken = forms.CharField(widget=forms.HiddenInput())


class SellStockForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
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
        fields = ["title", "cover_image", "sub_title", "description"]
        widgets = {
            "cover_image": forms.FileInput(
                attrs={"class": "news-file-upload-input form-input-field"}
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "news-title-input form-input-field",
                    "placeholder": "Enter Title",
                }
            ),
            "sub_title": forms.TextInput(
                attrs={
                    "class": "news-sub-title-input form-input-field",
                    "placeholder": "Enter Sub-Title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "news-description-input form-input-field",
                    "placeholder": "Enter News Description",
                }
            ),
        }
        exclude = ["publish_datetime"]

    title = forms.CharField(label="News Title", required=True, max_length=225)
    sub_title = forms.CharField(label="News Sub Title", required=False, max_length=225)
    description = forms.CharField(
        label="News Description", required=True, max_length=1000, widget=forms.Textarea
    )
    cover_image = forms.ImageField(label="Cover Image", required=False)


class FeedbackRatingForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["subject", "feedback", "rating"]


class NFTForm(forms.ModelForm):
    class Meta:
        model = NFT
        fields = [
            "image",
            "symbol",
            "description",
            "quantity",
            "is_for_sale",
            "current_price",
            "currency",
        ]

    def __init__(self, *args, **kwargs):
        super(NFTForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == "is_for_sale":
                pass
            else:
                field.widget.attrs["class"] = "form-control"


class BuyNFTForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    stripeToken = forms.CharField(widget=forms.HiddenInput())


class SellNFTForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    nft_symbol = forms.CharField(widget=forms.HiddenInput())


class StockFilterForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["current_price"]


class CurrencyConverterForm(forms.Form):
    amount = forms.DecimalField(
        min_value=0.01,
        label="Amount",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    currency_from = forms.ChoiceField(
        label="From Currency", widget=forms.Select(attrs={"class": "form-control"})
    )
    currency_to = forms.ChoiceField(
        label="To Currency", widget=forms.Select(attrs={"class": "form-control"})
    )

    def set_currency_choices(self, choices):
        self.fields["currency_from"].choices = choices
        self.fields["currency_to"].choices = choices


class GlossaryTermForm(forms.ModelForm):
    class Meta:
        model = GlossaryTerm
        fields = ["term", "definition"]


class TopicCreateForm(forms.ModelForm):
    class Meta:
        model = CourseCategory
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class SubjectCreateForm(forms.ModelForm):
    class Meta:
        model = Learn
        fields = ["title", "description", "category", "image"]
        exclude = ["slug"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = CourseCategory.objects.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.title)

        counter = 1
        while Learn.objects.filter(slug=instance.slug).exists():
            instance.slug = f"{slugify(instance.title)}-{counter}"
            counter += 1

        if commit:
            instance.save()
        else:
            return instance


class TransactionFilterForm(forms.Form):
    TYPE = [("BUY", "Buy"), ("SELL", "Sell")]

    transaction_type = forms.ChoiceField(
        label="Transaction Type",
        choices=[("", "All")] + TYPE,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    stock_symbol = forms.CharField(
        label="Search by Symbol",
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    start_date = forms.DateField(
        label="Start Date",
        required=False,
        widget=forms.TextInput(attrs={"type": "date", "class": "form-control"}),
    )

    end_date = forms.DateField(
        label="End Date",
        required=False,
        widget=forms.TextInput(attrs={"type": "date", "class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["stock_symbol"].widget.attrs.update(
            {"placeholder": "Symbol to search"}
        )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Start date cannot be greater than end date.")
