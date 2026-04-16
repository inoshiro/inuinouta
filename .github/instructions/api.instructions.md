---
applyTo: "inuinouta/video/apis.py,inuinouta/video/views.py,inuinouta/video/serializers.py,inuinouta/video/urls.py"
---

# API Instructions

## 基本方針

- API は Django REST Framework + dynamic-rest で構築している
- ルーティングは `DynamicRouter`（project `urls.py`）と `DefaultRouter`（app `urls.py`）を使用
- ReadOnly 系は `apis.py`（`WithDynamicViewSetMixin` + `ReadOnlyModelViewSet`）
- 書き込み系は `views.py`（`ModelViewSet`）

## エンドポイント追加・変更時の方針

### queryset

- 公開条件フィルタ（`is_open=True`, `is_member_only=False`）を必ず付ける
- `select_related` / `prefetch_related` で N+1 を防ぐ
- `PlaylistViewSet` のように `prefetch_related('items__song')` を活用する

### serializer 選択

- list と detail で異なるフィールドが必要なら、`get_serializer_class()` で切り替える
- 例: `VideoListSerializer`（一覧、`songs_count` 付き）/ `VideoDetailSerializer`（詳細、songs embed）
- 循環参照を避けるため、ネスト用に `VideoBasicSerializer` / `SongBasicSerializer` を使い分ける

### dynamic-rest の活用

- 既存エンドポイントは `DynamicModelSerializer` + `DynamicRelationField` で構築されている
- 新規の ReadOnly エンドポイントは既存パターンに寄せる
- `embed=True` でデフォルト展開、クライアント側で `?include[]` / `?exclude[]` も使える

### 権限

- 現状は認証不要の ReadOnly API + Playlist の CRUD
- 権限を追加する場合は ViewSet の `permission_classes` で制御する

## serializer でやってよいこと / やりすぎなこと

### やってよい

- フィールドの選択と除外
- `SerializerMethodField` での軽い加工（`songs_count` 等）
- `DynamicRelationField` でのリレーション制御
- `read_only` / `write_only` の切り替え
- `validate_*` でのバリデーション

### やりすぎ

- 外部 API 呼び出し（YouTube, S3）
- 複数モデルにまたがる複雑なトランザクション制御
- メール送信やファイル I/O

現状の `PlaylistSerializer.create()` / `update()` は nested write の範囲として許容するが、これ以上複雑化する場合は service 層への切り出しを検討する。

## nested write の扱い

- `PlaylistSerializer` が `items` の一括 create / update を担当している
- `update()` では既存 items を全削除→再作成する方式（replace 方式）
- この方式は現状のスケールでは問題ないが、アイテム数が大きくなる場合は差分更新を検討する

## レスポンス契約

- レスポンスのフィールド構成を変更する場合は、フロントエンド側への影響を確認する
- フィールドの削除・リネームは破壊的変更として扱い、テストを追加する
- フィールドの追加は後方互換なので、テストは推奨だが必須ではない
