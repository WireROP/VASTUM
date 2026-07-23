from django.contrib.auth.models import User
from django.db import models


class Channel(models.Model):
  owner = models.ForeignKey(
      User, on_delete=models.CASCADE, related_name='channels'
  )
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  banner = models.ImageField(upload_to='banners/', blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)


class Video(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField()
  channel = models.ForeignKey(
      Channel, on_delete=models.CASCADE, related_name='videos'
  )

  file_1080p = models.FileField(upload_to='videos/1080p/', blank=True, null=True)
  file_720p = models.FileField(upload_to='videos/720p/', blank=True, null=True)
  file_480p = models.FileField(upload_to='videos/480p/', blank=True, null=True)

  thumbnail = models.ImageField(upload_to='thumbnails/')
  duration = models.CharField(max_length=20, default='00:00')
  views = models.PositiveIntegerField(default=0)
  is_restricted = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-created_at']

  def __str__(self):
    return self.title


class Like(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('user', 'video')


class Comment(models.Model):
  video = models.ForeignKey(
      Video, on_delete=models.CASCADE, related_name='comments'
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)


class WatchHistory(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  video = models.ForeignKey(Video, on_delete=models.CASCADE)
  watched_at = models.DateTimeField(auto_now=True)