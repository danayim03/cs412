from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import User, Course, AcademicTrack, AcademicTrackCourse, ClassReview

# Home Page View
class HomePageView(TemplateView):
    template_name = 'project/home.html'

# Login View
class CustomLoginView(LoginView):
    template_name = 'project/login.html'

# Sign-Up View
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')  # Redirect to the login page
    else:
        form = UserCreationForm()
    return render(request, 'project/signup.html', {'form': form})


# User Views
class UserListView(ListView):
    model = User
    template_name = 'project/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('user_search', '')
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query)
            )
        return queryset


class UserDetailView(DetailView):
    model = User
    template_name = 'project/user_detail.html'
    context_object_name = 'user'


# Course Views
class CourseListView(ListView):
    model = Course
    template_name = 'project/course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('class_search', '')
        if search_query:
            queryset = queryset.filter(
                Q(course_name__icontains=search_query)
            )
        return queryset


class CourseDetailView(DetailView):
    model = Course
    template_name = 'project/course_detail.html'
    context_object_name = 'course'


# Academic Track Views
class AcademicTrackListView(ListView):
    model = AcademicTrack
    template_name = 'project/academictrack_list.html'
    context_object_name = 'academic_tracks'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('user_search', '')
        if search_query:
            queryset = queryset.filter(
                Q(user__username__icontains=search_query)
            )
        return queryset


class AcademicTrackDetailView(DetailView):
    model = AcademicTrack
    template_name = 'project/academictrack_detail.html'
    context_object_name = 'academic_track'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object.user

        classes_by_year = AcademicTrackCourse.objects.filter(
            academic_track__user=user
        ).order_by('year_taken', 'semester')

        grouped_classes = {
            "Freshman": [],
            "Sophomore": [],
            "Junior": [],
            "Senior": [],
        }
        for course in classes_by_year:
            grouped_classes[course.academic_track.year].append(course)

        context['grouped_classes'] = grouped_classes
        return context


class AcademicTrackYearView(ListView):
    model = AcademicTrack
    template_name = 'project/academictrack_year.html'
    context_object_name = 'academic_tracks'

    def get_queryset(self):
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
            queryset = queryset.filter(
                Q(course__course_name__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )
        return queryset


class ClassReviewDetailView(DetailView):
    model = ClassReview
    template_name = 'project/classreview_detail.html'
    context_object_name = 'class_review'
