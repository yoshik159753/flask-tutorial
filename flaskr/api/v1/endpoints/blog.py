import json
from http import HTTPStatus

from flask import Response, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource


class Blog(Resource):
    @jwt_required()
    def patch(self, blog_id):
        req = request.get_json()
        username = req.get('username')
        ret = {
            'blog_id': blog_id,
            'username': username,
        }
        return Response(json.dumps(ret),
                        mimetype="application/json",
                        status=HTTPStatus.OK)
