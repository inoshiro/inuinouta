# Generated by Django 3.2.9 on 2021-12-07 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0007_auto_20200917_0147'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='unplayable',
            field=models.BooleanField(default=False, verbose_name='再生出来ない動画'),
        ),
    ]
