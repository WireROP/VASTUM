from core.views import video_detail_view, video_list_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', video_list_view, name='video_list'),
    path('video/<int:pk>/', video_detail_view, name='video_detail'),
]

if settings.DEBUG:
  urlpatterns += static(
      settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
  )
