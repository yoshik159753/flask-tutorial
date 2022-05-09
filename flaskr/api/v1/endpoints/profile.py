from http import HTTPStatus

import requests
from flask import Response, current_app, request
from flask_restful import Resource


class Profile(Resource):

    def get(self):
        url = ""
        if request.args.get('lang') == 'en':
            url = current_app.config['PROFILE_URL_EN']
        else:
            url = current_app.config['PROFILE_URL']

        response = requests.get(url)

        return Response(response,
                        mimetype="text/plain",
                        status=HTTPStatus.OK)
