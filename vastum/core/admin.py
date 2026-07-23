from django.contrib import admin
from .models import Channel, Comment, Like, MoneroPayment, Video, WatchHistory


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
  list_display = ('name', 'owner', 'created_at')
  search_fields = ('name', 'owner__username')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
  list_display = ('title', 'channel', 'views', 'is_restricted', 'created_at')
  list_filter = ('is_restricted', 'created_at')
  search_fields = ('title', 'description')


@admin.register(MoneroPayment)
class MoneroPaymentAdmin(admin.ModelAdmin):
  list_display = (
      'user',
      'amount_xmr',
      'payment_type',
      'tx_hash',
      'is_confirmed',
      'created_at',
  )
  list_filter = ('is_confirmed', 'payment_type', 'created_at')
  search_fields = ('user__username', 'tx_hash')
  list_editable = ('is_confirmed',)


admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(WatchHistory)