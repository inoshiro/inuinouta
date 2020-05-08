from django.db import models
import os
import pyyoutube
import urllib.parse


class Channel(models.Model):
    name = models.CharField("チャンネル名", max_length=100)
    url = models.URLField("URL")
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = 'チャンネル'
        verbose_name_plural = 'チャンネル'

    def __str__(self):
        return self.name


class Video(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    title = models.CharField("タイトル", max_length=100, blank=True, null=True)
    url = models.URLField("URL")
    #type 歌動画か歌枠かの種別
    thumbnail = models.CharField("サムネイル", max_length=255, blank=True, null=True)
    published_at = models.DateTimeField("投稿日時", blank=True, null=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = '動画'
        verbose_name_plural = '動画'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            api_key = os.environ["YOUTUBE_API_KEY"]
            youtube_api = pyyoutube.Api(api_key=api_key)
            video_info = youtube_api.get_video_by_id(video_id=self.video_id)

            self.title = video_info.items[0].snippet.title
            self.published_at = video_info.items[0].snippet.publishedAt
        super(Video, self).save(*args, **kwargs)

    @property
    def sorted_song_set(self):
        return self.song_set.order_by('start_at')

    def video_id(self):
        qs = urllib.parse.urlparse(self.url).query
        return urllib.parse.parse_qs(qs)['v'][0]

    def number_of_songs(self):
        return self.song_set.count()


class Song(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    title = models.CharField("曲名", max_length=100, null=True)
    artist = models.CharField("アーティスト", max_length=100, blank=True, null=True)
    start_at = models.IntegerField("開始時間", default=0, null=True)
    end_at = models.IntegerField("終了時間", default=0, null=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = '楽曲'
        verbose_name_plural = '楽曲'

    def __str__(self):
        return self.title

    def get_queryset(self, *args, **kwargs):
        qs = Song.objects.annotate(
            video_published_at=models.Max('video__published_at')
        ).order_by('-video_published_at')
        return qs
