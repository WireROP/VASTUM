from django import forms
from .models import Video


class VideoUploadForm(forms.ModelForm):

  class Meta:
    model = Video
    fields = [
        'title',
        'description',
        'channel',
        'file_720p',
        'thumbnail',
        'duration',
    ]