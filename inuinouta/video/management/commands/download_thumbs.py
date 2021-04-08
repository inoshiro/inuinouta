from django.core.management.base import BaseCommand, CommandError
from video.models import Video
from video.utils import save_thumbnail


class Command(BaseCommand):
    help = 'Download video thumbnails'

    def add_arguments(self, parser):
        parser.add_argument('video_ids', nargs='*', type=str)

        parser.add_argument(
            '--all',
            action='store_true',
            help='Get all video thumbnails',
        )

        parser.add_argument(
            '--latest',
            action='store_true',
            help='Get latest video thumbnail'
        )

    def handle(self, *args, **options):
        if options['all']:
            videos = Video.objects.all()
            for v in videos:
                save_thumbnail(v.video_id())
                self._write_success('Download success: {}'.format(v.video_id()))
        elif options['latest']:
            v = Video.objects.latest('created_at')
            save_thumbnail(v.video_id())
            self._write_success('Download success: {}'.format(v.video_id()))
        else:
            if len(options['video_ids']) == 0:
                raise CommandError('Video ids are required')
            for video_id in options['video_ids']:
                try:
                    v = Video.objects.filter(url__endswith=video_id).get()
                except Video.DoesNotExist:
                    raise CommandError('Video "%s" does not exist' % video_id)
                save_thumbnail(v.video_id())
                self._write_success('Download success: {}'.format(v.video_id()))

    def _write_success(self, message):
        self.stdout.write(self.style.SUCCESS(message))

