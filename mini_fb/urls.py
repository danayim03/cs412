from django.urls import path
from . import views

urlpatterns = [
    path('mini_fb/', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),

]
