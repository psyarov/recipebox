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

urlpatterns = [
    path("", views.landing_view, name="landing"),
    path("about/", views.about_view, name="about"),
    path("register/", views.register_view, name="register"),

    # Public CBVs
    path("recipes/", views.RecipeListView.as_view(), name="recipe_list"),

    # ---- fixed string routes must come BEFORE the slug route ----
    path("recipes/create/", views.RecipeCreateView.as_view(), name="recipe_create"),
    path("recipes/<slug:slug>/edit/", views.RecipeUpdateView.as_view(), name="recipe_edit"),
    path("recipes/<slug:slug>/delete/", views.RecipeDeleteView.as_view(), name="recipe_delete"),
    # -------------------------------------------------------------

    path("recipes/<slug:slug>/", views.RecipeDetailView.as_view(), name="recipe_detail"),
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
]

