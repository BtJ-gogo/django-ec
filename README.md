# Book Store Application

Django で構築した書籍販売向け Web アプリケーションです。  
ユーザーはアカウントを作成し、商品（書籍）を閲覧・お気に入り登録できます。  

## 主な機能

- ユーザー認証（[django-allauth](https://django-allauth.readthedocs.io/en/latest/) 利用）
- 商品（書籍）一覧ページ / 詳細ページ
- 簡易検索機能
  - 書籍名、著者名による検索
- お気に入り登録・解除機能  
  - ワンクリックでお気に入りの追加/削除が可能  
- カート機能
- Stripe決済機能
- 購入履歴
- 配送先住所管理

## 動作環境

- Python 3.11+
- Django 5.x
- SQLite (開発用)
- Bootstrap 5 (フロントエンドデザイン)
- allauth (ユーザー管理)

## セットアップ方法

```bash
# リポジトリを取得
git clone <your-repo-url>
cd <your-project-folder>

# 仮想環境作成 & 有効化
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係インストール
pip install -r requirements.txt

# マイグレーション実行
python manage.py migrate

# 管理ユーザー作成
python manage.py createsuperuser

# 開発サーバー起動
python manage.py runserver
