from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_list")  # We'll adjust later if needed


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_allergen = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    prep_time_minutes = models.PositiveIntegerField()
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def clean(self):
        if self.prep_time_minutes <= 0:
            raise ValidationError("Preparation time must be greater than zero.")

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"slug": self.slug})


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50, blank=True)
    unit = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ("recipe", "ingredient")
        ordering = ["ingredient__name"]

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.ingredient.name}"


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.recipe}"
