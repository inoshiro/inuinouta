from .models import Video, Song, Playlist, PlaylistItem
from rest_framework import serializers
from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields import DynamicRelationField


class VideoSerializer(DynamicModelSerializer):
    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "url",
            "thumbnail_path",
            "is_open",
            "is_member_only",
            "is_stream",
            "unplayable",
            "published_at",
        ]


class SongSerializer(DynamicModelSerializer):
    class Meta:
        model = Song
        fields = ["video", "id", "title", "artist", "is_original", "start_at", "end_at"]

    video = DynamicRelationField("VideoSerializer")


class RandomSerializer(DynamicModelSerializer):
    class Meta:
        model = Song
        fields = ["video", "id", "title", "artist", "is_original", "start_at", "end_at"]

    video = DynamicRelationField("VideoSerializer", embed=True)


class PlaylistItemSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)
    song_id = serializers.PrimaryKeyRelatedField(
        source="song", queryset=Song.objects.all(), write_only=True
    )

    class Meta:
        model = PlaylistItem
        fields = ["id", "order", "song", "song_id"]


class PlaylistSerializer(serializers.ModelSerializer):
    items = PlaylistItemSerializer(many=True)

    class Meta:
        model = Playlist
        fields = ["id", "name", "description", "created_at", "items"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        playlist = Playlist.objects.create(**validated_data)
        for i, item in enumerate(items_data):
            PlaylistItem.objects.create(
                playlist=playlist, song=item["song"], order=item.get("order", i)
            )
        return playlist

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", [])
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        instance.items.all().delete()
        for i, item in enumerate(items_data):
            PlaylistItem.objects.create(
                playlist=instance, song=item["song"], order=item.get("order", i)
            )
        return instance
