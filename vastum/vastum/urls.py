from core.views import (
    login_view,
    logout_view,
    monero_payment_view,
    register_view,
    upload_video_view,
    video_detail_view,
    video_list_view,
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', video_list_view, name='video_list'),
    path('video/<int:pk>/', video_detail_view, name='video_detail'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('upload/', upload_video_view, name='upload_video'),
    path('pay/monero/', monero_payment_view, name='monero_pay'),
]

if settings.DEBUG:
  urlpatterns += static(
      settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
  )
