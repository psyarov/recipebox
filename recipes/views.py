from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from .forms import RegisterForm, RecipeForm, CommentForm, SearchForm, CategoryForm
from .models import Recipe, Category

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from .models import Recipe, Category, Comment, RecipeIngredient, Ingredient

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.db.models import Q

from .forms import RegisterForm, RecipeForm, CommentForm, SearchForm, CategoryForm, RecipeIngredientFormSet, IngredientForm








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
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset().select_related("author", "category")
        self.search_form = SearchForm(self.request.GET or None)
        if self.search_form.is_valid():
            q = self.search_form.cleaned_data.get("q")
            if q:
                qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search_form"] = getattr(self, "search_form", SearchForm())
        return ctx



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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            ctx["ingredient_formset"] = RecipeIngredientFormSet(self.request.POST)
        else:
            ctx["ingredient_formset"] = RecipeIngredientFormSet()
        return ctx

    def form_valid(self, form):
        # Save recipe with current user
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        form.save_m2m()

        # Bind and validate formset against this recipe
        formset = RecipeIngredientFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
            messages.success(self.request, "Recipe created successfully.")
            return redirect(self.object.get_absolute_url())
        # if formset has errors, re-render the page with errors
        return self.render_to_response(self.get_context_data(form=form, ingredient_formset=formset))



class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to edit this recipe.")
        return redirect("recipe_detail", slug=self.get_object().slug)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            ctx["ingredient_formset"] = RecipeIngredientFormSet(self.request.POST, instance=self.object)
        else:
            ctx["ingredient_formset"] = RecipeIngredientFormSet(instance=self.object)
        return ctx

    def form_valid(self, form):
        self.object = form.save()  # author is unchanged here
        formset = RecipeIngredientFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
            messages.success(self.request, "Recipe updated successfully.")
            return redirect(self.object.get_absolute_url())
        return self.render_to_response(self.get_context_data(form=form, ingredient_formset=formset))



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


class DashboardView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/dashboard.html"
    context_object_name = "recipes"
    paginate_by = 10

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user).select_related("category")

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "recipes/comment_form.html"  # we’ll reuse a simple form template

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        recipe = Recipe.objects.get(slug=self.kwargs["slug"])
        form.instance.recipe = recipe
        form.instance.author = self.request.user
        messages.success(self.request, "Comment added.")
        response = super().form_valid(form)
        # Always redirect to the recipe detail
        return redirect(recipe.get_absolute_url())

    def get_success_url(self):
        # Not used due to redirect in form_valid, but kept for safety
        return self.object.recipe.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "recipes/comment_confirm_delete.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to delete this comment.")
        return redirect(self.get_object().recipe.get_absolute_url())

    # ✅ Tell DeleteView where to go after success
    def get_success_url(self):
        return self.object.recipe.get_absolute_url()

    # (Optional) add a success message and call the parent delete
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()           # make sure self.object is set for get_success_url()
        messages.success(self.request, "Comment deleted.")
        return super().delete(request, *args, **kwargs)


# @method_decorator(login_required, name="dispatch")
# class DashboardView(TemplateView):
#     template_name = "recipes/dashboard.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["recipes"] = Recipe.objects.filter(author=self.request.user)
#         context["comments"] = Comment.objects.filter(author=self.request.user)
#         return context

class DashboardView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/dashboard.html"
    context_object_name = "recipes"
    paginate_by = 10

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add user's comments to the context so the template can render them
        context["comments"] = Comment.objects.filter(author=self.request.user).select_related("recipe")
        return context

class CategoryDetailView(ListView):
    model = Recipe
    template_name = "recipes/category_detail.html"
    context_object_name = "recipes"
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return (
            Recipe.objects
            .filter(category=self.category)
            .select_related("author", "category")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["category"] = self.category
        return ctx

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("landing")


class CategoryCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "recipes/category_form.html"
    success_url = reverse_lazy("category_list")

    def form_valid(self, form):
        messages.success(self.request, "Category created successfully.")
        return super().form_valid(form)


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "recipes/ingredient_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Ingredient created.")
        return super().form_valid(form)

    def get_success_url(self):
        # If the user came from a recipe form, send them back there
        nxt = self.request.GET.get("next") or self.request.POST.get("next")
        return nxt or reverse_lazy("recipe_list")
