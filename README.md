# README.md

## 概要

Flask のチュートリアルです。
[(Link)](https://flask.palletsprojects.com/en/2.0.x/tutorial/)

## 開発環境

| 項目     | 値                 |
| -------- | ------------------ |
| OS       | Ubuntu 20.04.1 LTS |
| 開発言語 | python 3.10.2      |

heroku の都合により python のバージョンは 3.10.2 以上としています。

## クイックスタート

### 使用するツール

- pyenv (python のバージョンが 3.10.2 以上であれば不要です)
- poetry

### usage

```bash
# 3.10.2 があることを確認
pyenv install --list
# 3.10.2 をインストール(リストになければ https://github.com/pyenv/pyenv-update を参考に pyenv をアップデート)
pyenv install 3.10.2

# 仮想環境の構築(ローカルの python が 3.10.2 以上の場合)
poetry env use system
# 仮想環境の構築(pyenv を使っている場合)
poetry env use /home/username/.pyenv/versions/3.10.2/bin/python
# 依存パッケージをインストール
poetry install

# 仮想環境の activate
poetry shell

export FLASK_APP=flaskr
export FLASK_ENV=development

# データ初期化
flask init-db

# (開発用) APP サーバー起動
flask run

# テスト実行
pytest

# カバレッジを取得しながらテスト実行
coverage run -m pytest
# 取得したカバレッジを html に出力
coverage html
```

#### 使用しているライブラリ

| 項目     | 値                                     |
| -------- | -------------------------------------- |
| Flask    | フレームワーク                         |
| autopep8 | 自動整形ツール                         |
| flake8   | ソースコードチェッカー                 |
| pytest   | ユニットテスト用ライブラリ             |
| coverage | ユニットテストのカバレッジ用ライブラリ |
| wheel    | Python パッケージ操作ライブラリ        |

## ディレクトリ構成

```txt
/home/user/Projects/flask-tutorial
├── flaskr/
│   ├── __init__.py
│   ├── db.py
│   ├── schema.sql
│   ├── auth.py
│   ├── blog.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── blog/
│   │       ├── create.html
│   │       ├── index.html
│   │       └── update.html
│   └── static/
│       └── style.css
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   ├── test_auth.py
│   └── test_blog.py
├── venv/
├── setup.py
└── MANIFEST.in
```

詳細は Flask のチュートリアルを参照してください。
[(Link)](https://flask.palletsprojects.com/en/2.0.x/tutorial/)
