from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, AcademicTrack

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'major', 'year_of_graduation')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year_of_graduation'].widget.attrs.update({'placeholder': 'YYYY-MM-DD'})

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'major', 'year_of_graduation')

class AcademicTrackForm(forms.ModelForm):
    class Meta:
        model = AcademicTrack
        fields = ('year',)