from .models import Video, Song
from rest_framework import serializers


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = ['video_id', 'title', 'url', 'thumbnail_path', 'is_open',
                  'is_member_only', 'unplayable', 'published_at']


class SongSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Song
        fields = ['video_id', 'title', 'artist', 'start_at', 'end_at']
