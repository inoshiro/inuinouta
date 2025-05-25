from django.contrib import admin
from django.db import models

from .models import Channel, Video, Song, Playlist, PlaylistItem


class ChannelAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


class SongInline(admin.TabularInline):
    model = Song
    template = "admin/video/video/edit_inline/tabular.html"


class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "number_of_songs", "published_at")
    ordering = ["-published_at"]
    inlines = [
        SongInline,
    ]


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
