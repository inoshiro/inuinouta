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
    title = models.CharField("タイトル", max_length=100)
    url = models.URLField("URL")
    #type 歌動画か歌枠かの種別
    thumbnail = models.CharField("サムネイル", max_length=255)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = '動画'
        verbose_name_plural = '動画'

    def __str__(self):
        return self.title
