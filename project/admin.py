from django.contrib import admin
from .models import User, Course, ClassReview, AcademicTrack, AcademicTrackCourse

admin.site.register(User)
admin.site.register(Course)
admin.site.register(ClassReview)
admin.site.register(AcademicTrack)
admin.site.register(AcademicTrackCourse)
