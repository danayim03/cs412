from django.shortcuts import get_object_or_404, redirect

# Create your views here.
from . models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, CreateStatusMessageForm
from django.urls import reverse
from .models import Profile, StatusMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404


# class-based view
class ShowAllProfilesView(ListView):
    '''A view to show all profiles.'''

    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    '''Display one profile selected at random'''

    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    '''A view to create a new profile.'''

    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    
    def get_success_url(self):
        '''Redirect to the profile page of the newly created profile.'''
        return self.object.get_absolute_url()
    
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''A view to create a new status message for a specific profile.'''

    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        '''Add the Profile object to the context data.'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context
    
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
    
    def form_valid(self, form):
        profile = self.get_object()
        form.instance.profile = profile
        sm = form.save()
        files = self.request.FILES.getlist('files')

        for file in files:
            image = Image(image_file=file, status_message=sm)
            image.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', args=[self.get_object().pk])
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''A view to update an existing profile.'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
    
    def get_success_url(self):
        '''Redirect to the profile page after the profile is updated.'''
        return reverse('show_profile', args=[self.object.pk])
    
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''A view to delete a specific status message.'''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        '''Redirect to the profile page after the status message is deleted.'''
        status_message = self.get_object()
        profile_id = status_message.profile.pk
        return reverse('show_profile', args=[profile_id])
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''A view to update an existing status message.'''
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        '''Redirect to the profile page after the status message is updated.'''
        status_message = self.get_object()
        profile_id = status_message.profile.pk
        return reverse('show_profile', args=[profile_id])
    
class CreateFriendView(LoginRequiredMixin, View):
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        other_profile = get_object_or_404(Profile, pk=self.kwargs['other_pk'])
        profile.add_friend(other_profile)
        return redirect('show_profile', pk=profile.pk)

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self):
        # Get the profile associated with the logged-in user
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_suggestions'] = self.get_object().get_friend_suggestions()
        return context

    
class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        # Get the profile associated with the logged-in user
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_feed'] = self.get_object().get_news_feed()
        return context
