from django.shortcuts import render, get_object_or_404

# Create your views here.
from . models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, CreateStatusMessageForm
from django.urls import reverse
from .models import Profile, StatusMessage

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
    
class CreateStatusMessageView(CreateView):
    '''A view to create a new status message for a specific profile.'''

    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        '''Add the Profile object to the context data.'''
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''Attach the Profile object to the status message.'''
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        form.instance.profile = profile
        sm = form.save()
        files = self.request.FILES.getlist('files')

        for file in files:
            image = Image(image_file=file, status_message=sm)
            image.save()

        return super().form_valid(form)

    def get_success_url(self):
        '''Redirect to the profile page for the profile related to this status message.'''
        return reverse('show_profile', args=[self.kwargs['pk']])
    
class UpdateProfileView(UpdateView):
    '''A view to update an existing profile.'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        '''Redirect to the profile page after the profile is updated.'''
        return reverse('show_profile', args=[self.object.pk])
    
class DeleteStatusMessageView(DeleteView):
    '''A view to delete a specific status message.'''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html' 
    context_object_name = 'status_message'

    def get_success_url(self):
        '''Redirect to the profile page after the status message is deleted.'''
        status_message = self.get_object()
        profile_id = status_message.profile.pk
        return reverse('show_profile', args=[profile_id])
    
class UpdateStatusMessageView(UpdateView):
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