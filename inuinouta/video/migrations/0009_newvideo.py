# Generated by Django 3.2.10 on 2021-12-28 05:10

from django.db import migrations, models
import django.db.models.deletion
import urllib.parse


def forwards_func(apps, schema_editor):
    Video = apps.get_model("video", "Video")
    NewVideo = apps.get_model("video", "NewVideo")
    db_alias = schema_editor.connection.alias
    new_videos = []

    for v in Video.objects.using(db_alias).all():
        qs = urllib.parse.urlparse(v.url).query
        video_id = urllib.parse.parse_qs(qs)['v'][0]
        new_videos.append(NewVideo(
            id=video_id,
            title=v.title,
            url=v.url,
            is_open=v.is_open,
            is_member_only=v.is_member_only,
            unplayable=v.unplayable,
            published_at=v.published_at,
            created_at=v.created_at,
            updated_at=v.updated_at,
            channel=v.channel
        ))

    NewVideo.objects.using(db_alias).bulk_create(new_videos)


def reverse_func(apps, schema_editor):
    NewVideo = apps.get_model("inuinouta", "NewVideo")
    db_alias = schema_editor.connection.alias
    NewVideo.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0008_video_unplayable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newvideo',
            fields=[
                ('id', models.CharField(max_length=16,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True,
                 max_length=100, null=True, verbose_name='タイトル')),
                ('url', models.URLField(verbose_name='URL')),
                ('is_open', models.BooleanField(
                    default=False, verbose_name='公開フラグ')),
                ('is_member_only', models.BooleanField(
                    default=False, verbose_name='メンバー限定')),
                ('unplayable', models.BooleanField(
                    default=False, verbose_name='再生出来ない動画')),
                ('published_at', models.DateTimeField(
                    blank=True, null=True, verbose_name='投稿日時')),
                ('created_at', models.DateTimeField(
                    auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(
                    auto_now=True, verbose_name='更新日時')),
                ('channel', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='video.channel')),
            ],
            options={
                'verbose_name': '動画',
                'verbose_name_plural': '動画',
                'ordering': ['-published_at'],
            },
        ),
        migrations.RunPython(
            forwards_func,
            reverse_func
        )
    ]
