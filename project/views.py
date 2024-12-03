from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
from .models import User, Course, AcademicTrack, AcademicTrackCourse, ClassReview
from django.db.models import Q


# Home Page View
class HomePageView(TemplateView):
    template_name = 'project/home.html'


# User Views
class UserListView(ListView):
    model = User
    template_name = 'project/user_list.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    template_name = 'project/user_detail.html'
    context_object_name = 'user'


# Course Views
class CourseListView(ListView):
    model = Course
    template_name = 'project/course_list.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'project/course_detail.html'
    context_object_name = 'course'


# Academic Track Views
class AcademicTrackListView(ListView):
    model = AcademicTrack
    template_name = 'project/academictrack_list.html'
    context_object_name = 'academic_tracks'


class AcademicTrackDetailView(DetailView):
    model = AcademicTrack
    template_name = 'project/academictrack_detail.html'
    context_object_name = 'academic_track'

    def get_context_data(self, **kwargs):
        # Get the base context
        context = super().get_context_data(**kwargs)

        # Get the user from the AcademicTrack instance
        user = self.object.user

        # Get the user's classes grouped by year
        classes_by_year = AcademicTrackCourse.objects.filter(
            academic_track__user=user
        ).order_by('year_taken', 'semester')

        # Group classes by year
        grouped_classes = {
            "Freshman": [],
            "Sophomore": [],
            "Junior": [],
            "Senior": [],
        }
        for course in classes_by_year:
            grouped_classes[course.academic_track.year].append(course)

        # Add the grouped classes to the context
        context['grouped_classes'] = grouped_classes
        return context
    
class AcademicTrackYearView(ListView):
    model = AcademicTrack
    template_name = 'project/academictrack_year.html'
    context_object_name = 'academic_tracks'

    def get_queryset(self):
        # Filter AcademicTrack objects based on the year passed in the URL
        return AcademicTrack.objects.filter(year=self.kwargs['year'])


# Class Review Views
class ClassReviewListView(ListView):
    model = ClassReview
    template_name = 'project/classreview_list.html'
    context_object_name = 'class_reviews'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('class_search', '')
        if search_query:
            # Allows searching by course name or author username
            queryset = queryset.filter(
                Q(course__course_name__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )
        return queryset


class ClassReviewDetailView(DetailView):
    model = ClassReview
    template_name = 'project/classreview_detail.html'
    context_object_name = 'class_review'
