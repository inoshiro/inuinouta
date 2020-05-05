from django.db import models


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
    title = models.CharField("タイトル", max_length=100, null=True)
    url = models.URLField("URL")
    #type 歌動画か歌枠かの種別
    thumbnail = models.CharField("サムネイル", max_length=255, null=True)
    published_at = models.DateTimeField("投稿日時", null=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = '動画'
        verbose_name_plural = '動画'

    def __str__(self):
        return self.title


class Song(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    title = models.CharField("曲名", max_length=100, null=True)
    artist = models.CharField("アーティスト", max_length=100, null=True)
    #start_at
    #end_at
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = '楽曲'
        verbose_name_plural = '楽曲'

    def __str__(self):
        return self.title
