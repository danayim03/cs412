from django.views.generic import ListView, DetailView, TemplateView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .models import CustomUser, Course, AcademicTrack, AcademicTrackCourse, ClassReview
from .forms import CustomUserCreationForm, EditProfileForm, AcademicTrackForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy


# Home Page View
class HomePageView(TemplateView):
    template_name = 'project/home.html'

    def dispatch(self, request, *args, **kwargs):
        # Redirect to login if user is not authenticated
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Add the profile edit form, pre-filled with current user data
        context['edit_profile_form'] = EditProfileForm(instance=user)
        # Add the academic track form
        context['academic_track_form'] = AcademicTrackForm()
        # Get academic tracks for the user
        context['academic_tracks'] = AcademicTrack.objects.filter(user=user)
        return context

    def post(self, request, *args, **kwargs):
        # Handle profile editing
        if 'edit_profile' in request.POST:
            profile_form = EditProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.add_message(request, messages.SUCCESS, 'Profile updated successfully.', extra_tags='profile_success')
            else:
                messages.add_message(request, messages.ERROR, 'Error updating profile.', extra_tags='profile_error')
        # Handle academic track addition
        elif 'add_academic_track' in request.POST:
            track_form = AcademicTrackForm(request.POST)
            if track_form.is_valid():
                new_track = track_form.save(commit=False)
                new_track.user = request.user  # Link to the logged-in user
                new_track.save()
                messages.success(request, 'Academic track added successfully.')
            else:
                messages.error(request, 'Error adding academic track.')
        return redirect('home_page')  # Replace 'home' with the correct home page URL name

class DeleteAcademicTrackView(View):
    def post(self, request, *args, **kwargs):
        track_id = kwargs.get('pk')
        track = get_object_or_404(AcademicTrack, pk=track_id, user=request.user)
        
        # Delete the track
        track.delete()

        # Add a success message
        messages.add_message(request, messages.SUCCESS, 'Academic track deleted successfully.', extra_tags='track_success')
        
        # Redirect back to the home page
        return redirect('home_page')
    
# Login View
class CustomLoginView(LoginView):
    template_name = 'project/login.html'

# Sign-Up View
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Correctly use CustomUserCreationForm
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')  # Redirect to the login page
    else:
        form = CustomUserCreationForm()
    return render(request, 'project/signup.html', {'form': form})

# User Views
class UserListView(ListView):
    model = CustomUser  # Use CustomUser instead of the default User model
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
    model = CustomUser
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
