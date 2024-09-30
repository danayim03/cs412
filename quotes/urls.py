# myproject/urls.py
# Modify your main project urls.py to include the quotes/urls.py file.
# quotes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),  # Root URL, displays a random quote and image
    path('quote/', views.random_quote, name='random_quote'),  # Random quote and image
    path('show_all/', views.show_all, name='show_all'),  # Show all quotes and images
    path('about/', views.about, name='about'),  # About page
]
