from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Recipe, Comment, Category
from django.utils.text import slugify


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "slug", "category", "prep_time_minutes", "image_url", "description"]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class SearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        max_length=100,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search recipes…", "class": "form-control"})
    )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug"]

    def clean_slug(self):
        slug = slugify(self.cleaned_data["slug"])
        if not slug:
            raise forms.ValidationError("Slug cannot be empty.")
        return slug

