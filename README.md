# Django EC Project

Django で構築した書籍販売向け Web アプリケーションです。  
商品閲覧からカート、注文、Stripe 決済まで、一通りの購買フローを実装しています。  

## 主な機能

- ユーザー認証（[django-allauth](https://django-allauth.readthedocs.io/en/latest/) 利用）
- 商品一覧・詳細表示
- 簡易検索機能
- お気に入り機能  
- カート機能
- Stripe決済
- 購入履歴の表示
- 配送先住所登録・管理
- Django Admin による商品管理

## 使用技術

- フロントエンド
  - Bootstrap 5.3
  - django-widget-tweaks
- バックエンド
  - Django 5.2.4
  - django-allauth
  - stripe
  - python-decouple
- データベース
  - SQLite
- プログラミング言語
  - Python 3.13  

## 画像について
- トップページの画像はUnsplashにあったもをリサイズして利用しております。

## セットアップ方法

```bash

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

