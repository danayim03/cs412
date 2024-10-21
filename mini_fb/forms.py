from django import forms
from .models import Profile, StatusMessage
from django.views.generic.edit import UpdateView
from django.urls import reverse


class CreateProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="City", required=True)
    email_address = forms.EmailField(label="Email Address", required=True)
    image_url = forms.URLField(label="Image URL", required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'image_url']

class CreateStatusMessageForm(forms.ModelForm):
    message = forms.CharField(label="Status Message", widget=forms.Textarea, required=True)

    class Meta:
        model = StatusMessage
        fields = ['message']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'email_address', 'image_url']
        
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', args=[self.object.pk])