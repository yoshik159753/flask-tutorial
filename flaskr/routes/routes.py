from flaskr.api.v1.endpoints.healthcheck import HealthCheckApi


def initialize_routes(api):
    api.add_resource(HealthCheckApi, '/api/v1/healthcheck')
