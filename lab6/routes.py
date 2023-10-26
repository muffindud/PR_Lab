from flask import jsonify

from __main__ import app
from models.electro_scooter import ElectroScooter


def template(scooter_id, scooter_name, scooter_battery_level):
    return {
        "id": scooter_id,
        "name": scooter_name,
        "battery_level": scooter_battery_level
    }


@app.route('/api/electro_scooters', methods=['GET'])
def get_all_electro_scooters():
    scooters = ElectroScooter.query.all()
    return jsonify([template(scooter.id, scooter.name, scooter.battery_level)] for scooter in scooters), 200


@app.route('/api/electro_scooters/<int:id>', methods=['GET'])
def get_electro_scooter_by_id(scooter_id):
    scooter = ElectroScooter.query.get(scooter_id)
    if scooter is None:
        return jsonify({"error": "Electro scooter not found"}), 404
    return jsonify(template(scooter.id, scooter.name, scooter.battery_level)), 200


# @app.route('/api/electro_scooters', methods=['POST'])
