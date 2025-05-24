from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from . import utils
import os
import pyyoutube
import urllib.parse

S3_THUMBNAIL_PATH = "https://inuinouta.s3.ap-northeast-1.amazonaws.com/images/thumbs/"


class Channel(models.Model):
    name = models.CharField("チャンネル名", max_length=100)
    url = models.URLField("URL")
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "チャンネル"
        verbose_name_plural = "チャンネル"

    def __str__(self):
        return self.name


class Video(models.Model):
    id = models.CharField("ID", max_length=16, primary_key=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    title = models.CharField("タイトル", max_length=100, blank=True, null=True)
    url = models.URLField("URL")
    is_open = models.BooleanField("公開フラグ", default=False)
    is_member_only = models.BooleanField("メンバー限定", default=False)
    is_stream = models.BooleanField("歌配信", default=True)
    unplayable = models.BooleanField("再生出来ない動画", default=False)
    published_at = models.DateTimeField("投稿日時", blank=True, null=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "動画"
        verbose_name_plural = "動画"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title:
            api_key = os.environ["YOUTUBE_API_KEY"]
            youtube_api = pyyoutube.Api(api_key=api_key)
            video_info = youtube_api.get_video_by_id(video_id=self.id)

            self.title = video_info.items[0].snippet.title
            self.published_at = video_info.items[0].snippet.publishedAt
        super(Video, self).save(*args, **kwargs)

    @property
    def sorted_song_set(self):
        return self.song_set.order_by("start_at")

    @property
    def thumbnail_path(self):
        return os.path.join(S3_THUMBNAIL_PATH, self.video_id + ".jpg")

    @property
    def video_id(self):
        qs = urllib.parse.urlparse(self.url).query
        return urllib.parse.parse_qs(qs)["v"][0]

    def number_of_songs(self):
        return self.song_set.count()


@receiver(post_save, sender=Video)
def save_thumbnail(sender, instance, created, **kwargs):
    if created:
        utils.save_thumbnail(instance.id)


@receiver(post_delete, sender=Video)
def delete_thumbnail(sender, instance, using, **kwargs):
    utils.delete_thumbnail(instance.id)


class Song(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    title = models.CharField("曲名", max_length=100, null=True)
    artist = models.CharField("アーティスト", max_length=100, blank=True, null=True)
    is_original = models.BooleanField("オリジナル", default=False)
    start_at = models.IntegerField("開始時間", default=0, null=True)
    end_at = models.IntegerField("終了時間", default=0, null=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "楽曲"
        verbose_name_plural = "楽曲"

    def __str__(self):
        return self.title

    def get_queryset(self, *args, **kwargs):
        qs = Song.objects.annotate(
            video_published_at=models.Max("video__published_at")
        ).order_by("-video_published_at")
        return qs


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # ユーザー紐付け（将来拡張）

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "プレイリスト"
        verbose_name_plural = "プレイリスト"


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(
        Playlist, on_delete=models.CASCADE, related_name="items"
    )
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]
        unique_together = ("playlist", "song")
        verbose_name = "プレイリスト楽曲"
        verbose_name_plural = "プレイリスト楽曲"
