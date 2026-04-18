---
name: heroku-deploy
description: >
  inuinouta バックエンドを Heroku へデプロイする際の標準手順。
  master ブランチへのマージ後、heroku コマンドを使って本番環境へ push する。
  「デプロイ」「Heroku push」「本番反映」などのキーワードで起動する。
---

# Heroku Deploy

inuinouta バックエンドを Heroku 本番環境へ反映する際の標準手順。

---

## 前提条件

- `heroku` CLI がインストール済みで `heroku login` 済みであること
- ローカルの `master` ブランチが最新であること（`git pull` 済み）
- デプロイ対象のブランチが master にマージ済みであること

参考: [Git を使用したデプロイ（Heroku Dev Center）](https://devcenter.heroku.com/ja/articles/git)

---

## Step 0: Heroku 認証・remote・SSH 鍵を確認する（初回または確認が必要なとき）

### ログイン状態の確認

```bash
heroku auth:whoami
```

未ログインの場合は `heroku login` を実行する。

### Heroku remote の確認・作成

```bash
git remote -v
```

`heroku  https://git.heroku.com/inui-no-uta.git` が表示されれば設定済み。  
未設定の場合は追加する:

```bash
heroku git:remote -a inui-no-uta
```

> **Heroku Git は HTTPS のみ対応（SSH は非対応）**  
> `git push heroku` は HTTPS で通信し、`heroku login` 時に `.netrc` へ保存された API キーで認証する。  
> **SSH 鍵の登録は `git push` には不要。**

### SSH 鍵の確認（`heroku run` を使う場合のみ）

`heroku run python ... migrate` などの dyno 実行では SSH 鍵が使われる場合がある。

```bash
heroku keys
```

未登録で dyno 接続が失敗する場合は追加する:

```bash
heroku keys:add ~/.ssh/id_ed25519.pub
```

---

## Step 1: master の最新化を確認する

```bash
git checkout master
git pull
git log --oneline -5
```

- 最新コミットがデプロイしたい変更を含んでいることを確認する
- 未マージの変更が残っていないかを確認する

---

## Step 2: ローカルでの動作確認（任意だが推奨）

```bash
make check
```

- `python manage.py check` と `python manage.py migrate --check` を一括実行
- エラーが出た場合はデプロイ前に修正する

---

## Step 3: Heroku へ push する

```bash
git push heroku master
```

- push 後は Ctrl+C でターミナルから切り離しても**ビルドはキャンセルされない**（バックグラウンドで継続）
- ビルド完了後に新しいリリースが自動作成される
- `bin/post_compile` が自動実行され `dynamic-rest` が `--no-deps` でインストールされる

---

## Step 4: マイグレーションを実行する

モデルの変更がある場合のみ実行する。

```bash
heroku run python inuinouta/manage.py migrate --app <app-name>
```

- マイグレーションが不要な場合はスキップしてよい
- 実行前にバックアップがあることが望ましい（本番 DB は PostgreSQL）

---

## Step 5: 動作確認

```bash
# ログをリアルタイムで確認する
heroku logs --tail --app <app-name>

# アプリを開く
heroku open --app <app-name>
```

- エラーログが出ていないかを確認する
- API エンドポイントへのアクセスが正常に返ることを確認する:
  - `/api/videos/`
  - `/api/songs/`

---

## よくあるエラーと対処

### `dynamic-rest` のインストール失敗

`bin/post_compile` が正常に動作しているか確認する。

```bash
heroku logs --app <app-name> | grep dynamic-rest
```

手動で実行する場合:
```bash
heroku run pip install --no-deps dynamic-rest==2.3.0 --app <app-name>
```

### マイグレーション競合

```bash
heroku run python inuinouta/manage.py showmigrations --app <app-name>
```

### 静的ファイルが更新されない

```bash
heroku run python inuinouta/manage.py collectstatic --noinput --app <app-name>
```

---

## ロールバック

デプロイ後に問題が発生した場合:

```bash
# 直前のリリースに戻す
heroku rollback --app <app-name>

# リリース一覧を確認する
heroku releases --app <app-name>
```

---

## 参照ファイル

- `Procfile` — gunicorn 起動設定
- `bin/post_compile` — dynamic-rest の --no-deps インストール
- `requirements.txt` — 本番依存パッケージ
- `inuinouta/inuinouta/settings.py` — 本番設定（`DEBUG=False`、`dj_database_url` で DB 接続）
