from core import views
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('', views.video_list_view, name='video_list'),
    path('video/<int:pk>/', views.video_detail_view, name='video_detail'),
]