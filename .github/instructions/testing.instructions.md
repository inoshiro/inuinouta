---
applyTo: "inuinouta/video/tests.py,inuinouta/**/test_*.py,inuinouta/**/tests/**"
---

# Testing Instructions

## テストランナー

- Django 標準の test runner を使用する
- pytest は現時点では未導入

```bash
# 全テスト実行
python inuinouta/manage.py test

# video app のみ
python inuinouta/manage.py test video

# 特定のテストクラス
python inuinouta/manage.py test video.tests.VideoApiTest
```

## テストの置き場所

- 現状は `inuinouta/video/tests.py` に集約（ほぼ空の状態）
- テストが増えたら `inuinouta/video/tests/` ディレクトリに分割してよい
  - `test_api_videos.py`, `test_api_songs.py`, `test_api_playlists.py` など
  - `__init__.py` を忘れないこと

## テスト方針

### まず守るライン

- 1 endpoint につき最低 1 happy path + 1 guard case
- happy path: 正常なリクエストで期待するフィールドが返ること
- guard case: 非公開動画がフィルタされること、存在しない ID で 404 が返ること、など

### API テストで守るべき観点

| 観点 | 何を確認するか |
| --- | --- |
| response shape | 返却フィールドが期待通りか（キーの存在、型） |
| filtering | `is_open=False` の動画が一覧に含まれないか |
| nested data | detail で songs が正しくネストされるか |
| nested write | Playlist の create / update で items が正しく保存されるか |

### 外部依存のモック

- YouTube Data API: `unittest.mock.patch` で `pyyoutube.Api` をモックする
- S3: `unittest.mock.patch` で `boto3.client` または `utils.save_thumbnail` / `utils.delete_thumbnail` をモックする
- テストで実際の外部 API を叩かない

```python
# 例: Video 作成時の YouTube API モック
from unittest.mock import patch, MagicMock

@patch('video.models.pyyoutube.Api')
def test_video_save(self, mock_api):
    mock_video_info = MagicMock()
    mock_video_info.items = [MagicMock(
        snippet=MagicMock(title='Test Title', publishedAt='2024-01-01T00:00:00Z')
    )]
    mock_api.return_value.get_video_by_id.return_value = mock_video_info
    # ...
```

```python
# 例: サムネイル保存のモック
@patch('video.models.utils.save_thumbnail')
@patch('video.models.utils.delete_thumbnail')
def test_video_signal(self, mock_delete, mock_save):
    # ...
```

## テストデータ

- `TestCase.setUp` または `setUpTestData` でテストデータを作成する
- fixture（JSON）は現状 `video_data.json` があるが、テストでは直接モデルを作成する方が明示的
- `Channel` → `Video` → `Song` の順に依存があるので、この順で作成する

## 現状の注意点

- `Video.save()` が YouTube API を叩くため、Video を作成するテストでは必ずモックが必要
- `post_save` signal で S3 に書き込むため、Video 作成テストでは `save_thumbnail` もモックする
- ローカルでは SQLite を使うため、PostgreSQL 固有の機能を使ったテストは本番で動くか注意する
