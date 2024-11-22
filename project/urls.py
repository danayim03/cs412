from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.HomePageView.as_view(), name='home_page'),
    
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
    path('classreviews/<int:pk>/', views.ClassReviewDetailView.as_view(), name='classreview_detail'),
]
