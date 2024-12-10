from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, DetailView, TemplateView, View, CreateView
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *

# Home Page View
class HomePageView(TemplateView):
    template_name = 'project/home.html'

    def dispatch(self, request, *args, **kwargs):
        # Redirect to login if user is not authenticated
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['edit_profile_form'] = EditProfileForm(instance=user)
        context['academic_track_form'] = AcademicTrackForm()
        context['academic_tracks'] = AcademicTrack.objects.filter(user=user)
        return context

    def post(self, request, *args, **kwargs):
        context = {}
        if 'edit_profile' in request.POST:
            profile_form = EditProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                context['profile_status'] = 'Profile updated successfully.'
            else:
                context['profile_status'] = 'Error updating profile.'
        elif 'add_academic_track' in request.POST:
            track_form = AcademicTrackForm(request.POST)
            if track_form.is_valid():
                new_track = track_form.save(commit=False)
                new_track.user = request.user  # Link to the logged-in user
                new_track.save()
                context['track_status'] = 'Academic track added successfully.'
            else:
                context['track_status'] = 'Error adding academic track.'
        return redirect('home_page')

# View for deleting an academic track
class DeleteAcademicTrackView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Query the AcademicTrack using pk and user
            track = AcademicTrack.objects.get(pk=kwargs.get('pk'), user=request.user)
        except AcademicTrack.DoesNotExist:
            # If not found, raise exception
            raise Exception("Academic track not found.")

        # Delete the object
        track.delete()

        # Redirect to the home page
        return redirect('home_page')

# Custom login view
class CustomLoginView(LoginView):
    template_name = 'project/login.html'

# Sign-up view for new users
def signup_view(request):
    context = {}
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            context['signup_status'] = 'Account created successfully. Please log in.'
            return redirect('login')
        else:
            context['signup_status'] = 'Error creating account.'

    else:
        form = CustomUserCreationForm()
    return render(request, 'project/signup.html', {'form': form})

# View for listing users with a search filter
class UserListView(ListView):
    model = CustomUser
    template_name = 'project/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        search_query = self.request.GET.get('user_search', '')
        queryset = super().get_queryset()
        if search_query:
            queryset = queryset.filter(username__icontains=search_query)
        return queryset

# Detailed view for a user's profile
class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'project/user_detail.html'
    context_object_name = 'user'

# View for listing courses with a search filter
class CourseListView(ListView):
    model = Course
    template_name = 'project/course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        search_query = self.request.GET.get('class_search', '')
        queryset = super().get_queryset()
        if search_query:
            queryset = queryset.filter(course_name__icontains=search_query)
        return queryset

# Detailed view for a course
class CourseDetailView(DetailView):
    model = Course
    template_name = 'project/course_detail.html'
    context_object_name = 'course'

# View for listing academic tracks with a user search filter
class AcademicTrackListView(ListView):
    model = AcademicTrack
    template_name = 'project/academictrack_list.html'
    context_object_name = 'academic_tracks'

    def get_queryset(self):
        search_query = self.request.GET.get('user_search', '')
        queryset = super().get_queryset()
        if search_query:
            queryset = queryset.filter(user__username__icontains=search_query)
        return queryset

# View for creating an academic track course
class AcademicTrackCourseCreateView(CreateView):
    model = AcademicTrackCourse
    template_name = 'project/edit_academic_track_course.html'
    fields = ['course', 'semester', 'year_taken']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Query the AcademicTrack object manually
            academic_track = AcademicTrack.objects.get(pk=self.kwargs['pk'])
        except AcademicTrack.DoesNotExist:
            # Raise exception if the AcademicTrack does not exist
            raise Exception("Academic track not found.")
        
        # Add the academic track and related courses to the context
        context['academic_track'] = academic_track
        context['courses'] = AcademicTrackCourse.objects.filter(academic_track=academic_track).select_related('course')
        return context

    def form_valid(self, form):
        try:
            # Query the AcademicTrack object manually
            academic_track = AcademicTrack.objects.get(pk=self.kwargs['pk'])
        except AcademicTrack.DoesNotExist:
            # Raise exception if the AcademicTrack does not exist
            raise Exception("Academic track not found.")
        
        # Attach the academic track to the form instance
        form.instance.academic_track = academic_track
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the edit page for the current academic track
        return reverse('edit_academic_track_course', kwargs={'pk': self.kwargs['pk']})
    
# Detailed view for an academic track, grouped by year and semester
class AcademicTrackDetailView(DetailView):
    model = AcademicTrack
    template_name = 'project/academictrack_detail.html'
    context_object_name = 'academic_track'

    def dispatch(self, request, *args, **kwargs):
        # Redirect to login if user is not authenticated
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AcademicTrack.DoesNotExist:
            raise Exception("No academic track found matching the query")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_tracks'] = AcademicTrack.objects.filter(user=self.object.user).order_by('year')
        courses = AcademicTrackCourse.objects.filter(academic_track=self.object).order_by('year_taken', 'semester')
        grouped_classes = {}
        for course in courses:
            year_semester = f"{course.year_taken} - {course.semester}"
            if year_semester not in grouped_classes:
                grouped_classes[year_semester] = []
            grouped_classes[year_semester].append(course)
        context['grouped_classes'] = grouped_classes
        return context

# View for deleting an academic track course
class DeleteAcademicTrackCourseView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Query the AcademicTrackCourse object manually
            course = AcademicTrackCourse.objects.get(id=kwargs['course_id'])
        except AcademicTrackCourse.DoesNotExist:
            # Raise exception if the AcademicTrackCourse does not exist
            raise Exception("Course not found.")
        
        # Get the associated academic track ID before deletion
        academic_track_id = course.academic_track.id
        
        # Delete the course
        course.delete()
        
        # Redirect to the edit page for the academic track
        return redirect('edit_academic_track_course', pk=academic_track_id)

# View for listing academic tracks by year
class AcademicTrackYearView(ListView):
    model = AcademicTrack
    template_name = 'project/academictrack_year.html'
    context_object_name = 'academic_tracks'

    def get_queryset(self):
        return AcademicTrack.objects.filter(year=self.kwargs['year'])

# View for listing class reviews and handling review submission
class ClassReviewListView(ListView):
    model = ClassReview
    template_name = 'project/classreview_list.html'
    context_object_name = 'class_reviews'

    def get_queryset(self):
        search_query = self.request.GET.get('class_search', '').strip()
        queryset = super().get_queryset()
        if search_query:
            queryset = queryset.filter(course__course_name__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ClassReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        context = self.get_context_data()
        if request.user.is_authenticated:
            form = ClassReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.author = request.user  # Set the author as the logged-in user
                review.save()
                context['status'] = "Your review has been submitted successfully."
            else:
                context['status'] = "There was an error with your submission. Please check the form and try again."
        else:
            context['status'] = "You must be logged in to submit a review."
        return self.render_to_response(context)

# Detailed view for a class review
class ClassReviewDetailView(DetailView):
    model = ClassReview
    template_name = 'project/classreview_detail.html'
    context_object_name = 'class_review'
