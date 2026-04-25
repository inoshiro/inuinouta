from unittest.mock import patch, MagicMock

from django.test import TestCase

from video.models import Channel, Video
from video import services


def _make_channel():
    return Channel.objects.create(name='テストチャンネル', url='https://www.youtube.com/@test')


def _make_video(channel, video_id='abc12345', title='テスト動画'):
    return Video.objects.create(
        id=video_id,
        channel=channel,
        title=title,
        url=f'https://www.youtube.com/watch?v={video_id}',
    )


class VideoSaveTest(TestCase):
    """Video.save() が外部 I/O を呼び出さないことを確認する。"""

    @patch('video.services.sync_thumbnail')
    def test_save_without_title_does_not_call_youtube(self, mock_sync):
        """title 未設定のまま保存しても YouTube API を呼ばない（DB 保存は成立する）。"""
        channel = _make_channel()
        video = Video(
            id='abc12345',
            channel=channel,
            url='https://www.youtube.com/watch?v=abc12345',
        )
        video.save()
        self.assertIsNone(video.title)
        self.assertTrue(Video.objects.filter(id='abc12345').exists())

    @patch('video.services.sync_thumbnail')
    def test_str_with_no_title_returns_id(self, mock_sync):
        """title が None のとき __str__ は id を返す。"""
        channel = _make_channel()
        video = Video(id='xyz99999', channel=channel, url='https://www.youtube.com/watch?v=xyz99999')
        video.save()
        self.assertEqual(str(video), 'xyz99999')


class SignalTest(TestCase):
    """post_save / post_delete signal が services 経由で動き、例外を飲み込むことを確認する。"""

    @patch('video.services.sync_thumbnail')
    def test_post_save_calls_sync_thumbnail_on_create(self, mock_sync):
        channel = _make_channel()
        video = _make_video(channel)
        mock_sync.assert_called_once_with(video.id)

    @patch('video.services.sync_thumbnail')
    def test_post_save_does_not_call_sync_thumbnail_on_update(self, mock_sync):
        channel = _make_channel()
        video = _make_video(channel)
        mock_sync.reset_mock()
        video.title = '更新後タイトル'
        video.save()
        mock_sync.assert_not_called()

    @patch('video.services.remove_thumbnail')
    @patch('video.services.sync_thumbnail')
    def test_post_delete_calls_remove_thumbnail(self, mock_sync, mock_remove):
        channel = _make_channel()
        video = _make_video(channel)
        video_id = video.id  # delete() 後は id が None になるため事前に保存
        video.delete()
        mock_remove.assert_called_once_with(video_id)

    @patch('video.services.sync_thumbnail', side_effect=Exception('S3 error'))
    def test_post_save_signal_absorbs_sync_error(self, mock_sync):
        """sync_thumbnail が失敗しても Video 作成自体は成功する。"""
        channel = _make_channel()
        # signal 内で例外が飲み込まれているため、ここで例外が出ないこと
        video = _make_video(channel)
        self.assertTrue(Video.objects.filter(id=video.id).exists())


class FetchAndApplyVideoMetaTest(TestCase):
    """services.fetch_and_apply_video_meta の動作を確認する。"""

    @patch('video.services.sync_thumbnail')
    @patch('video.services.pyyoutube.Api')
    def test_updates_title_and_published_at(self, mock_api_cls, mock_sync):
        channel = _make_channel()
        video = _make_video(channel, title=None)

        mock_info = MagicMock()
        mock_info.items = [MagicMock(
            snippet=MagicMock(title='Fetched Title', publishedAt='2024-06-01T00:00:00Z')
        )]
        mock_api_cls.return_value.get_video_by_id.return_value = mock_info

        services.fetch_and_apply_video_meta(video)

        video.refresh_from_db()
        self.assertEqual(video.title, 'Fetched Title')
        self.assertIsNotNone(video.published_at)

    @patch('video.services.sync_thumbnail')
    @patch('video.services.pyyoutube.Api')
    def test_raises_on_api_failure(self, mock_api_cls, mock_sync):
        """YouTube API 失敗時は例外を raise する（呼び出し元でハンドリング）。"""
        channel = _make_channel()
        video = _make_video(channel)

        mock_api_cls.return_value.get_video_by_id.side_effect = Exception('API error')

        with self.assertRaises(Exception):
            services.fetch_and_apply_video_meta(video)


class SyncThumbnailTest(TestCase):
    """services.sync_thumbnail / remove_thumbnail が例外を飲み込むことを確認する。"""

    @patch('video.utils.save_thumbnail', side_effect=Exception('S3 error'))
    def test_sync_thumbnail_absorbs_exception(self, mock_save):
        # 例外が外に出ないこと
        services.sync_thumbnail('someid')

    @patch('video.utils.delete_thumbnail', side_effect=Exception('S3 error'))
    def test_remove_thumbnail_absorbs_exception(self, mock_delete):
        services.remove_thumbnail('someid')

