# app.py
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from models.databse import db


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/scooters'

SWAGGER_URL = '/api/docs'
API_URL = '/static/openapi.json'


def main():
    db.init_app(app)

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Electro Scooters"
        }
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    import routes
    routes.init()
    app.run(debug=True)


if __name__ == '__main__':
    main()
