from django.urls import path
from . import views
from .views import (
    DeleteAcademicTrackView, 
    AcademicTrackCourseCreateView, 
    AcademicTrackDetailView, 
    HomePageView, 
    CustomLoginView, 
    UserListView, 
    UserDetailView, 
    CourseListView, 
    CourseDetailView, 
    AcademicTrackListView, 
    DeleteAcademicTrackCourseView,
    ClassReviewListView,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Homepage
    path('', HomePageView.as_view(), name='home_page'),
    path('delete_academic_track/<int:pk>/', DeleteAcademicTrackView.as_view(), name='delete_academic_track'),

    # Authentication routes
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', LogoutView.as_view(next_page='home_page'), name='logout'),

    # User-specific routes
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),

    # Course-specific routes
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),

    # Academic Track routes
    path('academictracks/', AcademicTrackListView.as_view(), name='academictrack_list'),
    path('academictracks/<int:pk>/', AcademicTrackDetailView.as_view(), name='academictrack_detail'),
    path('academictracks/<int:pk>/edit/', AcademicTrackCourseCreateView.as_view(), name='edit_academic_track_course'),
    path('academictracks/<int:pk>/delete-course/<int:course_id>/', DeleteAcademicTrackCourseView.as_view(), name='delete_academic_track_course'),

    # Class Review routes
    path('classreviews/', ClassReviewListView.as_view(), name='classreview_list'),
]
