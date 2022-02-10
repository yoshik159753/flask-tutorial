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


class HealthCheckApi(Resource):

    def get(self):
        db = get_db()
        with db.cursor() as cursor:
            # read
            cursor.execute('SELECT datetime FROM healthcheck WHERE id = 1')
            read_datetime_ = cursor.fetchone()
            if read_datetime_ is None:
                read_datetime = None
                # TODO: ログ出力
                # logger.info(dumps({'read_datetime': None}))
            else:
                read_datetime, = read_datetime_
                # TODO: ログ出力
                # logger.info(dumps({'read_datetime': healthcheck.datetime.isoformat()}))

            # write
            write_datetime = datetime.datetime.now(datetime.timezone.utc)
            cursor.execute(
                "INSERT INTO healthcheck (id, datetime) VALUES (1, %s)"
                " ON CONFLICT ON CONSTRAINT healthcheck_pkey"
                " DO UPDATE SET datetime=%s",
                (write_datetime, write_datetime,)
            )
        db.commit()

        # TODO: ログ出力
        # logger.info(dumps({'write': write_datetime.isoformat()}))

        ret = {
            'read_datetime': read_datetime,
            'write_datetime': write_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f'),
        }
        return Response(json.dumps(ret, default=default_handler),
                        mimetype="application/json",
                        status=200)
