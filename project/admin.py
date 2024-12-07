from django.contrib import admin
from .models import CustomUser, Course, ClassReview, AcademicTrack, AcademicTrackCourse

admin.site.register(CustomUser)
admin.site.register(Course)
admin.site.register(ClassReview)
admin.site.register(AcademicTrack)
admin.site.register(AcademicTrackCourse)
