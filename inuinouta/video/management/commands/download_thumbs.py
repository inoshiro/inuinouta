from django.core.management.base import BaseCommand
from video.models import Video
from video.utils import save_thumbnail


class Command(BaseCommand):
    help = 'Download all video thumbnails'

    def handle(self, *args, **options):
        videos = Video.objects.all()
        for v in videos:
            video_id = v.video_id()
            save_thumbnail(video_id)
            self.stdout.write(
                self.style.SUCCESS('Download success: {}'.format(video_id)))
