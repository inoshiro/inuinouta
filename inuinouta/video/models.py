from django.db import models
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


YOUTUBE_EMBED_BASE_URL = "https://www.youtube.com/embed/"

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
        verbose_name = '動画'
        verbose_name_plural = '動画'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            qs = urllib.parse.urlparse(self.url).query
            video_id = urllib.parse.parse_qs(qs)['v']

            youtube_api = pyyoutube.Api(api_key='AIzaSyBt9xjPse-_lzQTuqQeQ5wkaE-mqzLVa_A')
            video_info = youtube_api.get_video_by_id(video_id=video_id)

            self.title = video_info.items[0].snippet.title
            self.published_at = video_info.items[0].snippet.publishedAt
        super(Video, self).save(*args, **kwargs)

    def embedUrl(self):
        return YOUTUBE_EMBED_BASE_URL + self.url.split("=")[1]


class Song(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    title = models.CharField("曲名", max_length=100, null=True)
    artist = models.CharField("アーティスト", max_length=100, null=True)
    start_at = models.IntegerField("開始時間", null=True)
    end_at = models.IntegerField("終了時間", null=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = '楽曲'
        verbose_name_plural = '楽曲'

    def __str__(self):
        return self.title
