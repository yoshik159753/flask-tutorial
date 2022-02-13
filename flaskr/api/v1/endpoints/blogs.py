import datetime
import json

from flask import Response
from flask_restful import Resource
from flaskr.db import get_db


def default_handler(obj):
    """json.dumps の default 用ハンドラです。
    """
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError


class Blogs(Resource):
    def get(self):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT p.id, title, body, created, author_id, username'
                ' FROM posts p JOIN users u ON p.author_id = u.id'
                ' ORDER BY created DESC'
            )
            blogs_ = cursor.fetchall()
            blogs = []
            for blog in blogs_:
                id, title, body, created, author_id, username = blog
                blogs.append({
                    "id": id,
                    "title": title,
                    "body": body,
                    "created": created,
                    "author_id": author_id,
                    "username": username,
                })
            return Response(json.dumps(blogs, default=default_handler),
                            headers={'X-Total-Count': len(blogs)},
                            mimetype="application/json",
                            status=200)
