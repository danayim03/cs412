from django.urls import path
from . import views
from .views import DeleteAcademicTrackView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Homepage
    path('', views.HomePageView.as_view(), name='home_page'),
    path('delete_academic_track/<int:pk>/', DeleteAcademicTrackView.as_view(), name='delete_academic_track'),


    # Authentication routes
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', LogoutView.as_view(next_page='home_page'), name='logout'),

    # User-specific routes
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),

    # Course-specific routes
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),

    # Academic Track routes
    path('academictracks/', views.AcademicTrackListView.as_view(), name='academictrack_list'),
    path('academictracks/<int:pk>/', views.AcademicTrackDetailView.as_view(), name='academictrack_detail'),

    # Class Review routes
    path('classreviews/', views.ClassReviewListView.as_view(), name='classreview_list'),
]
