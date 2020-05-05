from django.contrib import admin

from .models import Channel, Video, Song


class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


class SongInline(admin.TabularInline):
    model = Song


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'published_at')
    inlines = [
        SongInline,
    ]


class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'video')


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Song, SongAdmin)
