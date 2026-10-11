import logging
import os

import pyyoutube

from . import utils

logger = logging.getLogger(__name__)


def fetch_and_apply_video_meta(video):
    """YouTube API からメタ情報を取得し Video の title / published_at を更新する。

    DB 保存（update_fields）まで行う。
    失敗した場合は例外をそのまま raise する（呼び出し元でハンドリングすること）。
    """
    api_key = os.environ['YOUTUBE_API_KEY']
    youtube_api = pyyoutube.Api(api_key=api_key)
    video_info = youtube_api.get_video_by_id(video_id=video.id)

    video.title = video_info.items[0].snippet.title
    video.published_at = video_info.items[0].snippet.publishedAt
    video.save(update_fields=['title', 'published_at', 'updated_at'])


def sync_thumbnail(video_id):
    """S3 にサムネイルを保存する。

    失敗した場合は例外を飲み込み warning ログを残す。
    """
    try:
        utils.save_thumbnail(video_id)
    except Exception:
        logger.warning('sync_thumbnail failed for video_id=%s', video_id, exc_info=True)


def remove_thumbnail(video_id):
    """S3 からサムネイルを削除する。

    削除失敗は warning ログのみ。DB 側の削除は成功扱いとする。
    """
    try:
        utils.delete_thumbnail(video_id)
    except Exception:
        logger.warning('remove_thumbnail failed for video_id=%s', video_id, exc_info=True)


class SongsTsvImportError(Exception):
    """TSV からの楽曲一括登録に失敗したときの例外。"""


def import_songs_from_tsv(video, text):
    """TSV テキスト（曲名<TAB>アーティスト<TAB>開始時間(秒)）から Song を一括登録する。

    1 行でもパースに失敗した場合は何も保存せず例外を送出する。
    """
    from .models import Song

    rows = []
    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        columns = line.split('\t')
        if len(columns) != 3:
            raise SongsTsvImportError(
                f'{line_no} 行目: 列数が3ではありません（曲名・アーティスト・開始時間（秒）の3列で入力してください）'
            )
        title, artist, start_at_raw = (c.strip() for c in columns)
        if not title:
            raise SongsTsvImportError(f'{line_no} 行目: 曲名が空です')
        try:
            start_at = int(start_at_raw)
        except ValueError:
            raise SongsTsvImportError(f'{line_no} 行目: 開始時間（秒）は整数で入力してください（{start_at_raw}）')
        rows.append(Song(video=video, title=title, artist=artist, start_at=start_at))

    if not rows:
        raise SongsTsvImportError('登録できる行がありません')

    Song.objects.bulk_create(rows)
    return len(rows)
