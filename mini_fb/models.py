from django.db import models
from django.utils import timezone
from django.urls import reverse

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
    
    def get_absolute_url(self):
        return reverse('show_profile', args=[str(self.pk)])
    
    def get_friends(self):
        friends_as_profile1 = Friend.objects.filter(profile1=self)
        friends_as_profile2 = Friend.objects.filter(profile2=self)

        friends = [friend.profile2 for friend in friends_as_profile1]  # Friends where self is profile1
        friends += [friend.profile1 for friend in friends_as_profile2]  # Friends where self is profile2

        return friends

# New StatusMessage model
class StatusMessage(models.Model):
    # Data attributes
    timestamp = models.DateTimeField(default=timezone.now)  # Automatically sets the current time as default
    message = models.TextField(blank=False)  # Text of the status message
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')  # Foreign key relationship

    def __str__(self):
        return f"Status by {self.profile} at {self.timestamp}: {self.message[:30]}"  # Return the first 30 chars of message
    
    def get_images(self):
        return Image.objects.filter(status_message=self)
    
class Image(models.Model):
    # Data attributes
    image_file = models.ImageField(blank=True) # an actual image
    timestamp = models.DateTimeField(default=timezone.now)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"Image for {self.status_message} uploaded at {self.timestamp}"
    
class Friend(models.Model):
    # Data attributes
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friends1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friends2')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
            return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"