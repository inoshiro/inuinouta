# Generated by Django 3.2.10 on 2021-12-28 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0012_remove_video'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='newvideo',
            new_name='video',
        ),
    ]
