## restaurant/urls.py
## description: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from . import views

# create a list of URLs for this app:
urlpatterns = [
    path(r'', views.main_page, name="main_page"),
    path(r'main/', views.main_page, name="main_page"),
    path(r'order/', views.order_page, name="order"),
    path(r'confirmation/', views.confirmation_page, name="confirmation"),
]
