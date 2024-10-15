from django.shortcuts import render

# Create your views here.
from . models import *
from django.views.generic import ListView
from django.views.generic import DetailView

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


