# app.py
from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_restful_swagger import swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
api = swagger.docs(
    Api(app),
    apiVersion='0.1',
    basePath='http://localhost:5000',
    resourcePath='/',
    produces=["application/json", "text/html"],
    api_spec_url='/api/spec',
    description='This is the API for the Electro Scooter project'
)

# SWAGGER_URL = "/api/docs"
# API_URL = "openapi.json"
# swagger_ui_blueprint = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': "API"
#     }
# )
# app.register_blueprint(swagger_ui_blueprint, url_preffix=SWAGGER_URL)


def main():
    import routes

    api.add_resource(routes.ElectroScooters, '/api/electro_scooters')
    # api.add_resource(routes.ElectroScooters, '/api/electro_scooters/<int:id>')

    app.run()


if __name__ == '__main__':
    main()
