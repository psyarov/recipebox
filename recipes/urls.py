# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path("", views.landing_view, name="landing"),
#     path("about/", views.about_view, name="about"),
#     path("register/", views.register_view, name="register"),
#
#     # Public CBVs
#     path("recipes/", views.RecipeListView.as_view(), name="recipe_list"),
#     path("recipes/<slug:slug>/", views.RecipeDetailView.as_view(), name="recipe_detail"),
#     path("categories/", views.CategoryListView.as_view(), name="category_list"),
#
#     path("recipes/create/", views.RecipeCreateView.as_view(), name="recipe_create"),
#     path("recipes/<slug:slug>/edit/", views.RecipeUpdateView.as_view(), name="recipe_edit"),
#     path("recipes/<slug:slug>/delete/", views.RecipeDeleteView.as_view(), name="recipe_delete"),
#
# ]

from django.urls import path
from . import views
from .views import DashboardView

urlpatterns = [
    path("", views.landing_view, name="landing"),
    path("about/", views.about_view, name="about"),
    path("register/", views.register_view, name="register"),

    # Public CBVs
    path("recipes/", views.RecipeListView.as_view(), name="recipe_list"),

    # Private routes BEFORE slug detail
    path("recipes/create/", views.RecipeCreateView.as_view(), name="recipe_create"),
    path("recipes/<slug:slug>/edit/", views.RecipeUpdateView.as_view(), name="recipe_edit"),
    path("recipes/<slug:slug>/delete/", views.RecipeDeleteView.as_view(), name="recipe_delete"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("recipes/<slug:slug>/comment/", views.CommentCreateView.as_view(), name="comment_create"),
    path("comments/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment_delete"),

    # Slug detail last
    path("recipes/<slug:slug>/", views.RecipeDetailView.as_view(), name="recipe_detail"),

    path("categories/", views.CategoryListView.as_view(), name="category_list"),

    path("dashboard/", DashboardView.as_view(), name="dashboard"),

    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path("categories/create/", views.CategoryCreateView.as_view(), name="category_create"),
    path("categories/<slug:slug>/", views.CategoryDetailView.as_view(), name="category_detail"),

]
