from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # Add this import

class User(AbstractUser):
    ROLE_CHOICES = [
        ('creator', 'Creator'),
        ('consumer', 'Consumer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='consumer')
    profile_picture_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

class Video(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    age_rating = models.CharField(max_length=20)
    file_path = models.CharField(max_length=255)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='videos')  # Changed

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')  # Changed
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.video.title}"

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')  # Changed
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')