from django.contrib import admin
from django.db import models

from .models import Channel, Video, Song, Playlist, PlaylistItem
from . import services


class ChannelAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


class SongInline(admin.TabularInline):
    model = Song
    template = "admin/video/video/edit_inline/tabular.html"


@admin.action(description='メタ情報を再取得する（YouTube API）')
def fetch_meta(modeladmin, request, queryset):
    success = 0
    failed = 0
    for video in queryset:
        try:
            services.fetch_and_apply_video_meta(video)
            success += 1
        except Exception as e:
            modeladmin.message_user(
                request,
                f'メタ取得失敗: {video.id} — {e}',
                level='warning',
            )
            failed += 1
    if success:
        modeladmin.message_user(request, f'{success} 件のメタ情報を更新しました。')


@admin.action(description='サムネイルを再同期する（S3）')
def sync_thumbs(modeladmin, request, queryset):
    success = 0
    for video in queryset:
        try:
            services.sync_thumbnail(video.id)
            success += 1
        except Exception as e:
            modeladmin.message_user(
                request,
                f'サムネイル同期失敗: {video.id} — {e}',
                level='warning',
            )
    if success:
        modeladmin.message_user(request, f'{success} 件のサムネイルを同期しました。')


class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "is_open", "is_stream", "number_of_songs", "published_at")
    list_filter = ("is_open", "is_stream", "is_member_only", "unplayable")
    search_fields = ("title", "id")
    ordering = ["-published_at"]
    inlines = [SongInline]
    actions = [fetch_meta, sync_thumbs]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change and not obj.title:
            # 新規登録かつ title 未設定のときにメタ取得を試みる
            try:
                services.fetch_and_apply_video_meta(obj)
            except Exception as e:
                self.message_user(
                    request,
                    f'YouTube メタ取得に失敗しました: {e}。admin action「メタ情報を再取得する」で再試行できます。',
                    level='warning',
                )


class SongAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "video")

    def get_queryset(self, request):
        qs = super(SongAdmin, self).get_queryset(request)
        qs = qs.annotate(video_published_at=models.Max("video__published_at")).order_by(
            "-video_published_at"
        )
        return qs


class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 1


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at")
    inlines = [PlaylistItemInline]


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(PlaylistItem)
