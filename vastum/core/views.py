from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import VideoUploadForm
from .models import Category, Video


def video_list_view(request):
  query = request.GET.get('q', '').strip()
  category_slug = request.GET.get('category', '').strip()
  sort_by = request.GET.get('sort', 'latest')
  restricted_mode = request.session.get('restricted_mode', False)

  videos = Video.objects.all()

  if restricted_mode:
    videos = videos.filter(is_restricted=False)

  if query:
    videos = videos.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )

  if category_slug:
    videos = videos.filter(category__slug=category_slug)

  if sort_by == 'most_viewed':
    videos = videos.order_by('-views')
  elif sort_by == 'top_rated':
    videos = videos.annotate(like_count=Count('likes')).order_by(
        '-like_count', '-created_at'
    )
  elif sort_by == 'longest':
    videos = videos.order_by('-duration')
  else:
    videos = videos.order_by('-created_at')

  paginator = Paginator(videos, 24)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  categories = Category.objects.all()

  context = {
      'videos': page_obj,
      'categories': categories,
      'query': query,
      'selected_category': category_slug,
      'sort_by': sort_by,
      'last_page': paginator.num_pages,
  }

  return render(request, 'core/index.html', context)


def video_detail_view(request, pk):
  video = get_object_or_404(Video, pk=pk)
  video.views += 1
  video.save(update_fields=['views'])

  related_videos = Video.objects.exclude(pk=video.pk)[:8]
  categories = Category.objects.all()
  context = {
      'video': video,
      'related_videos': related_videos,
      'categories': categories,
  }
  return render(request, 'core/video_detail.html', context)


def register_view(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('video_list')
  else:
    form = UserCreationForm()
  categories = Category.objects.all()
  return render(
      request, 'core/register.html', {'form': form, 'categories': categories}
  )


def login_view(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect('video_list')
  else:
    form = AuthenticationForm()
  categories = Category.objects.all()
  return render(
      request, 'core/login.html', {'form': form, 'categories': categories}
  )


def logout_view(request):
  logout(request)
  return redirect('video_list')


@login_required
def upload_video_view(request):
  if request.method == 'POST':
    form = VideoUploadForm(request.POST, request.FILES)
    if form.is_valid():
      video = form.save(commit=False)
      if video.channel.owner == request.user:
        video.save()
        return redirect('video_list')
  else:
    form = VideoUploadForm()
  categories = Category.objects.all()
  return render(
      request, 'core/upload.html', {'form': form, 'categories': categories}
  )


@login_required
def monero_payment_view(request):
  platform_monero_address = (
      '888888888888888888888888888888888888888888888888888888888888888888888888888888'
  )
  categories = Category.objects.all()
  context = {
      'monero_address': platform_monero_address,
      'categories': categories,
  }
  return render(request, 'core/monero_pay.html', context)