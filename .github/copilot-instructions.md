# Copilot カスタム指示

## プロジェクト概要

- `いぬいのうた` のバックエンド API
- 戌亥とこさんの歌動画・楽曲データを管理し、フロントエンド（Nuxt 4）へ REST API を提供する
- 主要 app は `video`（Channel, Video, Song, Playlist, PlaylistItem）

## 技術スタック

- **フレームワーク**: Django 4.2
- **API**: Django REST Framework + dynamic-rest
- **DB**: PostgreSQL（本番）/ SQLite（ローカル）
- **外部サービス**: YouTube Data API（動画メタ取得）、AWS S3（サムネイル保存）
- **デプロイ**: Heroku（gunicorn）
- **モニタリング**: Sentry

## ディレクトリ構成

```
inuinouta/          # Django project root（manage.py がここ）
├── inuinouta/      # project config（settings, urls, wsgi）
├── video/          # 主要 app
│   ├── models.py
│   ├── serializers.py
│   ├── apis.py     # DRF ViewSet（ReadOnly 系）
│   ├── views.py    # テンプレート view + PlaylistViewSet
│   ├── urls.py     # app 内ルーティング
│   ├── utils.py    # 外部 I/O ヘルパー（S3, YouTube サムネイル）
│   ├── admin.py
│   ├── tests.py
│   └── management/commands/
├── templates/
└── static/
```

## コーディングスタイル

- PEP 8 準拠
- シングルクォートを基本とする（既存コードに合わせる）
- UI 文言は日本語、コード識別子とコメントは英語
- Django の verbose_name は日本語

## 責務の置き場所（要約）

| ファイル | 責務 |
| --- | --- |
| `models.py` | 永続化ルール、ドメイン表現 |
| `serializers.py` | 入出力変換、バリデーション |
| `apis.py` | ReadOnly な API ViewSet（dynamic-rest） |
| `views.py` | テンプレート view、ModelViewSet |
| `utils.py` | 外部 I/O ヘルパー |
| signal（`models.py` 内） | サムネイル保存・削除の副作用 |

詳細は `.github/instructions/*.md` を参照。

## Issue 対応の基本フロー

1. 調査・方針共有: 変更前に影響範囲と確認方法をユーザーに共有する
2. 実装: 作業ブランチ上で小さく変更する
3. テスト: `python inuinouta/manage.py test` で確認する
4. レビュー依頼: ユーザーに変更内容を提示する
5. commit & push

## 現状の注意点

- `Video.save()` に YouTube API 呼び出しが入っている（タイトル・投稿日の自動取得）
- `post_save` / `post_delete` signal でサムネイル S3 保存・削除をしている
- `PlaylistSerializer` が nested write（create / update）を直接担当している
- `tests.py` はほぼ空。テストは今後整備していく段階
- これらは既知の技術的負債であり、段階的に改善する方針

## 詳細ルールへの入口

- アーキテクチャ: `.github/instructions/architecture.instructions.md`
- API 実装: `.github/instructions/api.instructions.md`
- テスト: `.github/instructions/testing.instructions.md`
