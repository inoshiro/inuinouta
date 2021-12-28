# Generated by Django 3.2.10 on 2021-12-28 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0010_song_newvideo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='video',
        ),
        migrations.AlterField(
            model_name='song',
            name='newvideo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.newvideo'),
        ),
    ]
