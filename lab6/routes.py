# routes.py
from flask import jsonify, request
from flask_restful import Api, Resource
from __main__ import app, api, swagger

from models.databse import db
from models.electro_scooter import ElectroScooter


@app.route('/api/docs')
def spec():
    return jsonify(swagger(app))


class ElectroScooters(Resource):
    @swagger.operation(
        notes='Get all electro scooters',
        responseClass=ElectroScooter.__name__,
        nickname='get',
        parameters=[
            {
                "name": "id",
                "description": "Electro scooter identifier",
                "required": True,
                "allowMultiple": False,
                "dataType": 'int',
                "paramType": "path"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Electro scooter found"
            },
            {
                "code": 404,
                "message": "Electro scooter not found"
            }
        ]
    )
    def get(self, id=None):
        if id is None:
            scooters = ElectroScooter.query.all()
            return jsonify([scooter.serialize() for scooter in scooters])
        else:
            scooter = ElectroScooter.query.filter_by(id=id).first()
            if scooter is None:
                return {'message': 'Electro scooter not found'}, 404
            else:
                return jsonify(scooter.serialize())

    def post(self):
        ...




