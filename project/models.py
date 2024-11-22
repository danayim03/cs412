from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    major = models.CharField(max_length=255)
    year_of_graduation = models.DateField()

    def __str__(self):
        return self.username

class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    description = models.TextField()
    credits = models.IntegerField()

    def __str__(self):
        return self.course_name

class AcademicTrack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.CharField(max_length=50, choices=[
        ("Freshman", "Freshman"),
        ("Sophomore", "Sophomore"),
        ("Junior", "Junior"),
        ("Senior", "Senior"),
    ])

    def __str__(self):
        return f"{self.user.username}'s {self.year} Track"

class AcademicTrackCourse(models.Model):
    academic_track = models.ForeignKey(AcademicTrack, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20, choices=[
        ("Fall", "Fall"),
        ("Spring", "Spring"),
        ("Summer", "Summer"),
    ])
    year_taken = models.IntegerField()

    def __str__(self):
        return f"{self.academic_track} - {self.course.course_name} ({self.semester} {self.year_taken})"

class ClassReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    difficulty = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review_text = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    recommend_to_take = models.BooleanField()

    def __str__(self):
        return f"Review by {self.author.username} for {self.course.course_name}"
