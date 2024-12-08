from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, AcademicTrack, AcademicTrackCourse, ClassReview

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

class AcademicTrackCourseForm(forms.ModelForm):
    class Meta:
        model = AcademicTrackCourse
        fields = ['academic_track', 'course', 'semester', 'year_taken']

class ClassReviewForm(forms.ModelForm):
    class Meta:
        model = ClassReview
        fields = ['course', 'rating', 'difficulty', 'review_text', 'recommend_to_take']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'recommend_to_take': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }