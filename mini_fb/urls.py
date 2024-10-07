from django.urls import path
from . import views

urlpatterns = [
    path('/mini_fb/', views.random_quote, name='show_all_profiles'),
    path('home/', views.show_all, name='show_all'),  # Show all quotes and images
    path('about/', views.about, name='about'),  # About page
]
