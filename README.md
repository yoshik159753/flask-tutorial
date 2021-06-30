# README.md

## 概要

Flask のチュートリアルです。
[(Link)](https://flask.palletsprojects.com/en/2.0.x/tutorial/)

## 開発環境

| 項目     | 値                 |
| -------- | ------------------ |
| OS       | Ubuntu 20.04.1 LTS |
| 開発言語 | python 3.8         |

## クイックスタート

### 使用するツール

- pyenv (python のバージョンが 3.8 であれば不要です)
- pipenv

### usage

```bash
pipenv --python 3.8
pipenv install Flask
pipenv install --dev autopep8 flake8

export FLASK_APP=flaskr
export FLASK_ENV=development

flask init-db

flask run
```

#### 使用しているライブラリ

| 項目     | 値                     |
| -------- | ---------------------- |
| Flask    | フレームワーク         |
| autopep8 | 自動整形ツール         |
| flake8   | ソースコードチェッカー |

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
