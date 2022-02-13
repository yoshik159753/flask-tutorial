from flaskr.api.v1.endpoints.healthcheck import HealthCheckApi
from flaskr.api.v1.endpoints.blogs import Blogs


def initialize_routes(api):
    api.add_resource(HealthCheckApi, '/api/v1/healthcheck')

    api.add_resource(Blogs, '/api/v1/blog')
