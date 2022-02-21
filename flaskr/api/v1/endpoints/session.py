import datetime
import json
from http import HTTPStatus

import jwt
from flask import Response, current_app, request
from flask_restful import Resource
from werkzeug.security import check_password_hash

from flaskr.db import get_db


def default_handler(obj):
    """json.dumps の default 用ハンドラです。
    """
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError


class Session(Resource):

    def post(self):
        req = request.get_json()
        username = req.get('username')
        password = req.get('password')

        # TODO: バリデーションチェック

        error_code = None

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM users WHERE username = %s', (username,)
            )
            user = cursor.fetchone()

            if user is None:
                error_code = 1
            else:
                user_id, user_username, user_password = user
                if not check_password_hash(user_password, password):
                    error_code = 1

        if error_code is not None:
            ret = {'error_code': error_code}
            return Response(json.dumps(ret, default=default_handler),
                            mimetype="application/json",
                            status=HTTPStatus.BAD_REQUEST)

        # cookie にセットするセッション管理用の jwt を生成
        payload = {
            'sub': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        }
        token = jwt.encode(
            payload=payload,
            key=current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )

        response = Response(mimetype="application/json",
                            status=200)
        response.set_cookie(key=current_app.config.get('SESSION_COOKIE_NAME'),
                            value=token,
                            httponly=current_app.config.get('SESSION_COOKIE_HTTPONLY'))
        # TODO: for production
        # response.set_cookie(key="token", value="token", httponly=True, secure=True)
        return response
