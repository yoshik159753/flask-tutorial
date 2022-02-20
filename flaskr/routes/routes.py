from flaskr.api.v1.endpoints.blogs import Blogs
from flaskr.api.v1.endpoints.healthcheck import HealthCheckApi
from flaskr.api.v1.endpoints.session import Session


def initialize_routes(api):
    api.add_resource(HealthCheckApi, '/api/v1/healthcheck')

    api.add_resource(Session, '/api/v1/session')

    api.add_resource(Blogs, '/api/v1/blog')
