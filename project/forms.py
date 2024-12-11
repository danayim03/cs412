# project/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, AcademicTrack, AcademicTrackCourse, ClassReview

# Form for user registration with custom fields and placeholder customization for year of graduation.
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'major', 'year_of_graduation')

    def __init__(self, *args, **kwargs):
        # Initialize the form by calling the parent class's __init__ method.
        super().__init__(*args, **kwargs)
        # Update the 'year_of_graduation' field's widget attributes to include a placeholder.
        # Source for placeholder: Django Widgets Documentation (Django Form Fields)
        self.fields['year_of_graduation'].widget.attrs.update({'placeholder': 'YYYY-MM-DD'})

# Form for editing user profile, using the same fields as CustomUser.
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'major', 'year_of_graduation')

# Form for creating or editing an academic track, with a field for the year.
class AcademicTrackForm(forms.ModelForm):
    class Meta:
        model = AcademicTrack
        fields = ('year',)

# Form for creating or editing an academic track course, including the academic track, course, semester, and year taken.
class AcademicTrackCourseForm(forms.ModelForm):
    class Meta:
        model = AcademicTrackCourse
        fields = ['academic_track', 'course', 'semester', 'year_taken']

# Form for submitting a class review, with fields for course, rating, difficulty, review text, and recommendation.
class ClassReviewForm(forms.ModelForm):
    class Meta:
        model = ClassReview
        fields = ['course', 'rating', 'difficulty', 'review_text', 'recommend_to_take']
        # Customizing the widgets for the form fields
        # Source: Customizing Widget Instances (Django Form and Field Validation)
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'recommend_to_take': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
