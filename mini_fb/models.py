from django.db import models
from django.utils import timezone

# Profile model (original code)
class Profile(models.Model):
    # data attributes:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.EmailField(unique=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_status_messages(self):
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')

# New StatusMessage model
class StatusMessage(models.Model):
    # Data attributes
    timestamp = models.DateTimeField(default=timezone.now)  # Automatically sets the current time as default
    message = models.TextField(blank=False)  # Text of the status message
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')  # Foreign key relationship

    def __str__(self):
        return f"Status by {self.profile} at {self.timestamp}: {self.message[:30]}"  # Return the first 30 chars of message
