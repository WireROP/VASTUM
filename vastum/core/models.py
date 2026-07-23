from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
  name = models.CharField(max_length=100, unique=True)
  slug = models.SlugField(max_length=100, unique=True)

  class Meta:
    verbose_name_plural = 'Categories'
    ordering = ['name']

  def __str__(self):
    return self.name


class Channel(models.Model):
  owner = models.ForeignKey(
      User, on_delete=models.CASCADE, related_name='channels'
  )
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  banner = models.ImageField(upload_to='banners/', blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name


class Video(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField()
  channel = models.ForeignKey(
      Channel, on_delete=models.CASCADE, related_name='videos'
  )
  category = models.ForeignKey(
      Category,
      on_delete=models.SET_NULL,
      null=True,
      blank=True,
      related_name='videos',
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

  def __str__(self):
    return f'{self.user.username} on {self.video.title}'


class WatchHistory(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  video = models.ForeignKey(Video, on_delete=models.CASCADE)
  watched_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'{self.user.username} watched {self.video.title}'


class MoneroPayment(models.Model):
  PAYMENT_TYPES = (
      ('AD', 'Advertisement Boost'),
      ('SUB', 'Platform Subscription / Tip'),
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  amount_xmr = models.DecimalField(max_digits=18, decimal_places=8)
  payment_type = models.CharField(max_length=3, choices=PAYMENT_TYPES)
  tx_hash = models.CharField(max_length=255, unique=True)
  is_confirmed = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.user.username} - {self.amount_xmr} XMR'