from django.contrib import admin
from .models import Category, Ingredient, Recipe, RecipeIngredient, Comment


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "prep_time_minutes", "created_at")
    list_filter = ("category", "author")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [RecipeIngredientInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_filter = ("is_allergen",)
    search_fields = ("name",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("recipe", "author", "created_at")
    search_fields = ("text",)


# Register RecipeIngredient explicitly (optional for admin view)
@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "quantity", "unit")
