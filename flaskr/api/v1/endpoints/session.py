import datetime
import json
from http import HTTPStatus

from flask import Response, request
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required, set_access_cookies,
                                unset_jwt_cookies)
from flask_restful import Resource
from flaskr.db import get_db
from werkzeug.security import check_password_hash


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

        ret = {
            'user_id': user_id,
            'username': user_username,
        }
        response = Response(json.dumps(ret),
                            mimetype="application/json",
                            status=HTTPStatus.OK)
        access_token = create_access_token(identity=user_id)
        print(access_token)
        set_access_cookies(response, access_token)

        return response

    def delete(self):
        response = Response(mimetype="application/json",
                            status=200)
        unset_jwt_cookies(response)
        return response

    @jwt_required()
    def get(self):
        if (get_jwt_identity() is None):
            return Response(mimetype="application/json",
                            status=HTTPStatus.UNAUTHORIZED)
        return Response(mimetype="application/json",
                        status=HTTPStatus.OK)
