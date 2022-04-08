from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies
import datetime
import json
from http import HTTPStatus
from flask_jwt_extended import jwt_required

import jwt
from flask import Response, current_app, request
from flask_restful import Resource
from werkzeug.security import check_password_hash

from flaskr.db import get_db


class CsrfToken(Resource):

    def get(self):
        csrf_token = request.cookies.get(current_app.config.get('JWT_ACCESS_CSRF_COOKIE_NAME'))
        ret = {'csrf-token': csrf_token}
        response = Response(json.dumps(ret),
                            mimetype="application/json",
                            status=HTTPStatus.OK)
        return response
