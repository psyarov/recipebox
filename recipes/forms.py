from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Recipe

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "slug", "category", "prep_time_minutes", "image_url", "description"]
