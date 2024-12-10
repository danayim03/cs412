from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user model extending Django's AbstractUser to include additional fields like major and graduation year.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)  # Ensuring username is unique
    email = models.EmailField(unique=True)  # Ensuring email is unique
    major = models.CharField(max_length=255, blank=True, null=True)  # User's field of study
    year_of_graduation = models.DateField(blank=True, null=True)  # Year of graduation

    def __str__(self):
        return self.username

# Model representing a course with attributes like course code, name, department, and credits.
class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)  # Unique code for each course
    course_name = models.CharField(max_length=255)  # Name of the course
    department = models.CharField(max_length=255)  # Department that offers the course
    description = models.TextField()  # Course description (FYI: copied from BU websites)
    credits = models.IntegerField()  # Number of credits for the course

    def __str__(self):
        return self.course_name

# Model for an academic track, linked to a user and specifying the year (such as Freshman, Sophomore, etc).
class AcademicTrack(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User associated with the track
    year = models.CharField(max_length=50, choices=[
        ("Freshman", "Freshman"),
        ("Sophomore", "Sophomore"),
        ("Junior", "Junior"),
        ("Senior", "Senior"),
    ])  # Year of study

    def __str__(self):
        return f"{self.user.username}'s {self.year} Track"

# Model representing the association between an academic track and courses taken, including semester and year.
class AcademicTrackCourse(models.Model):
    academic_track = models.ForeignKey(AcademicTrack, on_delete=models.CASCADE)  # Academic track
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Course associated with the track
    semester = models.CharField(max_length=20, choices=[
        ("Fall", "Fall"),
        ("Spring", "Spring"),
        ("Summer", "Summer"),
    ])  # Semester when the course was taken
    year_taken = models.IntegerField()  # Year when the course was taken (such as 2024, 2025, etc).

    def __str__(self):
        return f"{self.academic_track} - {self.course.course_name} ({self.semester} {self.year_taken})"

# Model for class reviews, linking courses to user authors and including review details like rating and difficulty.
class ClassReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Course being reviewed
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User who wrote the review
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating score from 1 to 5
    difficulty = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Difficulty score from 1 to 5
    review_text = models.TextField()  # Detailed review content
    date_posted = models.DateField(auto_now_add=True)  # Date the review was posted
    recommend_to_take = models.BooleanField()  # Whether the course is recommended

    def __str__(self):
        return f"Review by {self.author.username} for {self.course.course_name}"
