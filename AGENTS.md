# inuinouta Agent Guide

## Project Brief

- `いぬいのうた` のバックエンド API（Django + DRF + dynamic-rest）
- フロントエンド（Nuxt 4）に対して動画・楽曲・プレイリストの REST API を提供する
- 主要 app は `video`。モデルは `Channel`, `Video`, `Song`, `Playlist`, `PlaylistItem`
- GitHub の主対象リポジトリは `inoshiro/inuinouta`

## Role Split

- **Codex**: 要件整理、設計検討、影響範囲の特定、実装方針の提案
- **Copilot**: 実装、テスト追加、リファクタリング、コード補完

## Working Principles

- いきなり広い変更をしない。まず問題設定とスコープを揃える
- 1 task = 1 文脈 / 1 デプロイ判断
- 複数案があるときは推奨案と却下理由を短く示す
- 変更前に影響範囲と確認方法を整理する

## Backend Discipline

### 責務分離

| レイヤー | 責務 | やりすぎ注意 |
| --- | --- | --- |
| `models.py` | 永続化ルール、ドメイン表現 | 外部 API 呼び出し、重い副作用 |
| `serializers.py` | 入出力変換、バリデーション | 複雑な更新手順、ビジネスロジック |
| `apis.py` / `views.py` | HTTP 入出力、queryset 制御 | 業務ロジックの集中 |
| `utils.py` | 外部 I/O ヘルパー（S3, YouTube） | 状態変更、DB 操作 |
| signal | 補助的な副作用（サムネイル保存等） | 主要フローの起点 |

### 守るべきルール

- API レスポンス型と UI 都合の整形責務を混ぜない
- 外部 I/O（YouTube API, S3）を安易に model.save や signal に増やさない
- 新しい外部 I/O は `utils.py` または将来の `services/` に置く
- queryset のフィルタ条件（`is_open`, `is_member_only`）は API の公開契約。変更は慎重に

## Replanning Trigger

- 同じアプローチで 2 回以上失敗したら一度立ち止まる
- 立ち止まったら: ①分かった事実 ②未確定な点 ③有力な仮説 ④次の 1 手 を整理する
- 3 回連続で前進しないなら、人間への確認を優先する

## Instruction Entry Points

- 常時読む横断ルール: `.github/copilot-instructions.md`
- アーキテクチャ: `.github/instructions/architecture.instructions.md`
- API 実装: `.github/instructions/api.instructions.md`
- テスト: `.github/instructions/testing.instructions.md`
