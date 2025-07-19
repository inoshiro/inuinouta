from .models import Video, Song
from .serializers import (
    VideoListSerializer,
    VideoDetailSerializer,
    SongSerializer,
    RandomSerializer,
)
from django.http import HttpResponse
from rest_framework.viewsets import ReadOnlyModelViewSet
from dynamic_rest.viewsets import WithDynamicViewSetMixin


class VideoViewSet(WithDynamicViewSetMixin, ReadOnlyModelViewSet):
    queryset = Video.objects.filter(is_member_only=False)
    serializer_class = VideoListSerializer  # デフォルトは一覧用

    def get_serializer_class(self):
        """一覧表示と詳細表示で異なるシリアライザーを使用"""
        if self.action == "retrieve":
            return VideoDetailSerializer
        return VideoListSerializer


class SongViewSet(WithDynamicViewSetMixin, ReadOnlyModelViewSet):
    queryset = Song.objects.filter(video__is_member_only=False)
    serializer_class = SongSerializer


class RandomViewSet(WithDynamicViewSetMixin, ReadOnlyModelViewSet):
    queryset = Song.objects.order_by("?").filter(video__is_member_only=False)
    serializer_class = RandomSerializer
