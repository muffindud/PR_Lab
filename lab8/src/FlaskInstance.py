# src/FlaskInstance.py

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from models.databse import db


app = Flask(__name__)


class FlaskInstance:
    def __init__(
            self,
            host: str,
            port: int,
            db_uri: str,
            role: str,
            token: str
    ):
        self.SWAGGER_URL: str = '/api/docs'
        self.API_URL: str = '/static/openapi.json'
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        app.config['ROLE'] = role
        app.config['TOKEN'] = token

        self.host: str = host
        self.port: int = port

        db.init_app(app)

        self.swagger_ui_blueprint = get_swaggerui_blueprint(
            self.SWAGGER_URL,
            self.API_URL,
            config={
                'app_name': "Electro Scooters"
            }
        )
        app.register_blueprint(
            self.swagger_ui_blueprint,
            url_prefix=self.SWAGGER_URL
        )

        from src import routes
        routes.init()

        app.run(
            host=self.host,
            port=self.port,
            debug=False,
            use_reloader=False
        )
