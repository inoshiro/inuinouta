from .models import Video, Song
from .serializers import VideoSerializer, SongSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from dynamic_rest.viewsets import WithDynamicViewSetMixin


class VideoViewSet(WithDynamicViewSetMixin, ReadOnlyModelViewSet):
    queryset = Video.objects.filter(is_menber_only=False)
    serializer_class = VideoSerializer


class SongViewSet(WithDynamicViewSetMixin, ReadOnlyModelViewSet):
    queryset = Song.objects.filter(video__is_member_only=False)
    serializer_class = SongSerializer
