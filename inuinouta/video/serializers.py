from .models import Video, Song
from rest_framework import serializers
from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields import DynamicRelationField


class VideoSerializer(DynamicModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'url', 'thumbnail_path', 'is_open',
                  'is_member_only', 'unplayable', 'published_at']


class SongSerializer(DynamicModelSerializer):
    class Meta:
        model = Song
        fields = ['video', 'id', 'title', 'artist', 'start_at', 'end_at']

    video = DynamicRelationField('VideoSerializer')
