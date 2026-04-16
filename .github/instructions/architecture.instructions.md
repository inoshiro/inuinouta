---
applyTo: "inuinouta/video/**"
---

# Architecture Instructions

## ファイルごとの責務

### `models.py` — 永続化ルールとドメイン表現

- フィールド定義、リレーション、`Meta`（ordering, verbose_name）、`__str__`、シンプルな property
- **やりすぎ注意**: 外部 API 呼び出し、ファイル I/O、重い副作用
- 現状 `Video.save()` に YouTube API 呼び出しがある。これは既存動作として残すが、新規で同様のパターンを増やさない
- 新しいモデルを追加するときは `Meta.verbose_name` を日本語で付ける

### `serializers.py` — 入出力変換とバリデーション

- DRF / dynamic-rest の serializer でフィールド選択、ネスト、read/write 制御を行う
- `SerializerMethodField` は表示用の軽い加工に使ってよい
- **やりすぎ注意**: 複雑な更新手順、外部 API 呼び出し、複数モデルにまたがるトランザクション制御
- 現状 `PlaylistSerializer` が nested write（create / update）を担当している。大きく複雑化する場合は将来 service 層への切り出しを検討する

### `apis.py` — ReadOnly API ViewSet

- `WithDynamicViewSetMixin` + `ReadOnlyModelViewSet` で読み取り専用 API を提供する
- `get_serializer_class()` で list / detail のシリアライザーを切り替える
- queryset には公開条件フィルタ（`is_open=True`, `is_member_only=False`）を付ける
- **やりすぎ注意**: 業務ロジックをここに集中させない

### `views.py` — テンプレート view と書き込み系 ViewSet

- テンプレート描画（`all_in_one`）と `PlaylistViewSet`（ModelViewSet）を配置
- 新しい書き込み系エンドポイントは原則ここか、app 内の別ファイルに置く

### `utils.py` — 外部 I/O ヘルパー

- S3 操作（`save_thumbnail`, `delete_thumbnail`）、YouTube サムネイルダウンロード
- DB 操作や状態変更は入れない。純粋な外部 I/O ヘルパーに留める

### signal（`models.py` 内）

- `post_save` / `post_delete` で `utils.py` のサムネイル操作を呼び出している
- signal は補助的な副作用に使い、新規の主要フローを signal 起点にしない
- 新しい signal を追加する前に、その処理が本当に signal で行うべきか検討する

## 将来の拡張方針

### `services/` ディレクトリ

- 今すぐ必須にはしないが、以下のケースが出てきたら `video/services.py` または `video/services/` を導入する:
  - 外部 API 呼び出し + DB 更新が絡む処理
  - 複数モデルにまたがるトランザクション
  - view / serializer から呼ばれる共通のビジネスロジック
- 導入時は view → service → model の依存方向を守る

## 新規実装チェックリスト

コードを追加・変更するときは以下を確認する:

- [ ] 責務を置くファイルは適切か（上の表を参照）
- [ ] model.save に外部 I/O を増やしていないか
- [ ] serializer に複雑なロジックを押し込んでいないか
- [ ] queryset の公開条件フィルタ（`is_open`, `is_member_only`）を維持しているか
- [ ] signal を新しい主要フローの起点にしていないか
