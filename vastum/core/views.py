from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from .models import Video


def video_list_view(request):
  query = request.GET.get('q', '').strip()
  sort_by = request.GET.get('sort', 'latest')
  restricted_mode = request.session.get('restricted_mode', False)

  videos = Video.objects.all()

  if restricted_mode:
    videos = videos.filter(is_restricted=False)

  if query:
    videos = videos.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )

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

  context = {
      'videos': page_obj,
      'query': query,
      'sort_by': sort_by,
      'last_page': paginator.num_pages,
  }

  return render(request, 'core/index.html', context)


def video_detail_view(request, pk):
  video = get_object_or_404(Video, pk=pk)
  video.views += 1
  video.save(update_fields=['views'])

  related_videos = Video.objects.exclude(pk=video.pk)[:8]

  context = {'video': video, 'related_videos': related_videos}

  return render(request, 'core/video_detail.html', context)