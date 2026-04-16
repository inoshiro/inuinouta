# いぬいのうた

にじさんじ所属のバーチャルライバー戌亥とこの歌動画を視聴しやすくするための Web サイト。

戌亥とこさんの歌を楽曲単位でも動画・歌枠単位でも見つけて、気持ちよく聴き続けられるファン向けアプリのバックエンド API。

## 技術スタック

- Django 4.2 / Django REST Framework / dynamic-rest
- PostgreSQL（本番）/ SQLite（ローカル）
- YouTube Data API / AWS S3
- Heroku（gunicorn）/ Sentry

## セットアップ

```bash
# 仮想環境の作成と有効化
python -m venv env
source env/bin/activate

# 依存パッケージのインストール
pip install -r requirements.txt

# ローカル設定
# inuinouta/inuinouta/local_settings.py を作成し、SECRET_KEY や DB 設定を記述する

# マイグレーション
python inuinouta/manage.py migrate

# 開発サーバ起動
python inuinouta/manage.py runserver
```

## 開発コマンド

```bash
# 開発サーバ
python inuinouta/manage.py runserver

# テスト実行
python inuinouta/manage.py test

# video app のテストのみ
python inuinouta/manage.py test video

# 管理コマンド: サムネイルダウンロード
python inuinouta/manage.py download_thumbs --all
python inuinouta/manage.py download_thumbs --latest
python inuinouta/manage.py download_thumbs <video_id>

# Django admin
python inuinouta/manage.py createsuperuser
```

## ディレクトリ構成

```
inuinouta/              # Django project root（manage.py がここ）
├── inuinouta/          # project config（settings, urls, wsgi）
├── video/              # 主要 app
│   ├── models.py       # Channel, Video, Song, Playlist, PlaylistItem
│   ├── serializers.py  # DRF / dynamic-rest serializers
│   ├── apis.py         # ReadOnly API ViewSet
│   ├── views.py        # テンプレート view + PlaylistViewSet
│   ├── urls.py         # app 内ルーティング
│   ├── utils.py        # 外部 I/O ヘルパー（S3, YouTube）
│   ├── admin.py        # Django admin 設定
│   ├── tests.py        # テスト（整備中）
│   └── management/commands/
│       └── download_thumbs.py
├── templates/
└── static/
```

## API エンドポイント

| パス | ViewSet | 説明 |
| --- | --- | --- |
| `/api/videos/` | `VideoViewSet` (ReadOnly) | 動画一覧・詳細 |
| `/api/songs/` | `SongViewSet` (ReadOnly) | 楽曲一覧・詳細 |
| `/api/random/` | `RandomViewSet` (ReadOnly) | ランダム楽曲 |
| `/api/playlists/` | `PlaylistViewSet` (CRUD) | プレイリスト管理 |

## AI 協働ルール

AI エージェント（Copilot / Codex）と協働する際は、以下を参照してください:

- **AGENTS.md** — エージェントの役割分担と基本方針
- **.github/copilot-instructions.md** — 常時読む横断ルール
- **.github/instructions/** — ファイル種別ごとの詳細ルール
  - `architecture.instructions.md` — 責務分離の指針
  - `api.instructions.md` — API 実装の方針
  - `testing.instructions.md` — テストの方針と実行方法

## デプロイ

Heroku へデプロイ。`Procfile` で gunicorn を起動する。

```
web: gunicorn --chdir inuinouta inuinouta.wsgi --log-file -
```
