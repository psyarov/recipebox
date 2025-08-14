from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_view, name="landing"),
    path("about/", views.about_view, name="about"),
    path("register/", views.register_view, name="register"),
]
