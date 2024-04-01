from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("access", views.access, name="access"),
    path("parking", views.parking, name="parking"),
    path("advanced-booking", views.advanced_booking, name="advanced-booking"),
    path("about", views.about, name="about"),
    path("my-admin", views.my_admin, name="my-admin"),
    path("signin", views.signin, name="signin"),
]
