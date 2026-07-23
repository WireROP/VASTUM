from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_list_view, name='video_list'),
    path('video/<int:pk>/', views.video_detail_view, name='video_detail'),
    path('upload/', views.upload_video_view, name='upload_video'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('fund-xmr/', views.monero_payment_view, name='fund_xmr'),
]