# Generated by Django 3.2.10 on 2021-12-28 05:40

from django.db import migrations, models
import django.db.models.deletion
import urllib.parse


def forwards_func(apps, schema_editor):
    Newvideo = apps.get_model("video", "Newvideo")
    Song = apps.get_model("video", "Song")
    db_alias = schema_editor.connection.alias

    for s in Song.objects.using(db_alias).all():
        qs = urllib.parse.urlparse(s.video.url).query
        video_id = urllib.parse.parse_qs(qs)['v'][0]
        nv = Newvideo.objects.using(db_alias).get(id=video_id)
        s.newvideo = nv
        s.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0009_newvideo'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='newvideo',
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='video.newvideo'),
        ),
        migrations.RunPython(
            forwards_func,
            reverse_func
        )
    ]
