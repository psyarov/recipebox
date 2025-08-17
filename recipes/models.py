from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.core.validators import MinValueValidator



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})



class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_allergen = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


from django.core.validators import MinValueValidator
# ...existing imports...

class Recipe(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=220, unique=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    prep_time_minutes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def clean(self):
        # double safety; form validator already ensures >=1 via MinValueValidator
        if self.prep_time_minutes is not None and self.prep_time_minutes <= 0:
            raise ValidationError("Preparation time must be greater than zero.")

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"slug": self.slug})


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50, blank=True)
    unit = models.CharField(max_length=50, blank=True)

    class Meta:
        # keep the legacy constraint but give it a name (better admin/errors)
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient"
            )
        ]
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
