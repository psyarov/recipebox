from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .forms import RegisterForm
from .models import Recipe, Category

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import RecipeForm
from .models import Recipe, Category



def landing_view(request):
    return render(request, "landing.html")


def about_view(request):
    return render(request, "about.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Your account has been created. You are now logged in.")
            login(request, user)
            return redirect("landing")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/recipe_list.html"
    context_object_name = "recipes"
    paginate_by = 10  # simple pagination

    def get_queryset(self):
        qs = super().get_queryset().select_related("author", "category")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(description__icontains=q)
        return qs


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class CategoryListView(ListView):
    model = Category
    template_name = "recipes/category_list.html"
    context_object_name = "categories"
    ordering = ["name"]


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_form.html"

    def form_valid(self, form):
        # Assign current user as author
        form.instance.author = self.request.user
        messages.success(self.request, "Recipe created successfully.")
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to edit this recipe.")
        return redirect("recipe_detail", slug=self.get_object().slug)

    def form_valid(self, form):
        messages.success(self.request, "Recipe updated successfully.")
        return super().form_valid(form)


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = "recipes/recipe_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("recipe_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to delete this recipe.")
        return redirect("recipe_detail", slug=self.get_object().slug)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Recipe deleted successfully.")
        return super().delete(request, *args, **kwargs)

