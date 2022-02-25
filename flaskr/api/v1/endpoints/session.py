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

        ret = {
            'user_id': user_id,
            'username': user_username,
        }
        response = Response(json.dumps(ret),
                            mimetype="application/json",
                            status=HTTPStatus.OK)
        response.set_cookie(key=current_app.config.get('SESSION_COOKIE_NAME'),
                            value=token,
                            httponly=current_app.config.get('SESSION_COOKIE_HTTPONLY'),
                            secure=current_app.config.get('SESSION_COOKIE_SECURE'),
                            samesite=current_app.config.get('SESSION_COOKIE_SAMESITE'))
        # TODO: for production
        # response.set_cookie(key="token", value="token", httponly=True, secure=True)
        return response

    def delete(self):
        response = Response(mimetype="application/json",
                            status=200)
        response.delete_cookie(key=current_app.config.get('SESSION_COOKIE_NAME'))
        return response

    def get(self):
        try:
            session_jwt = request.cookies.get(current_app.config.get('SESSION_COOKIE_NAME'))
            jwt.decode(session_jwt,
                       key=current_app.config.get('SECRET_KEY'),
                       algorithms=['HS256'])

        except jwt.exceptions.ExpiredSignatureError:
            ret = {'error_code': 1}
            return Response(json.dumps(ret),
                            mimetype="application/json",
                            status=HTTPStatus.UNAUTHORIZED)

        except jwt.exceptions.InvalidTokenError:
            return Response(mimetype="application/json",
                            status=HTTPStatus.UNAUTHORIZED)

        return Response(mimetype="application/json",
                        status=HTTPStatus.OK)
