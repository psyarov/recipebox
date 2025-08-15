from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_view, name="landing"),
    path("about/", views.about_view, name="about"),
    path("register/", views.register_view, name="register"),

    # Public CBVs
    path("recipes/", views.RecipeListView.as_view(), name="recipe_list"),
    path("recipes/<slug:slug>/", views.RecipeDetailView.as_view(), name="recipe_detail"),
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
]
