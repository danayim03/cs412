from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
    path('status/create_status/', views.CreateStatusMessageView.as_view(), name='create_status'),  # Updated
    path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),  # Updated
    path('status/<int:pk>/delete/', views.DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update/', views.UpdateStatusMessageView.as_view(), name='update_status'),
    path('profile/add_friend/<int:other_pk>/', views.CreateFriendView.as_view(), name='add_friend'),  # Updated
    path('profile/friend_suggestions/', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),  # Updated
    path('profile/news_feed/', views.ShowNewsFeedView.as_view(), name='news_feed'),  # Updated

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'),
]
