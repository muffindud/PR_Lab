# src/routes.py
from json import loads, dumps

import requests
from flask import jsonify, request

from __main__ import app
from models.databse import db
from models.electro_scooter import ElectroScooter


def init():
    pass


def template(scooter_id, scooter_name, scooter_battery_level):
    return {
        "id": scooter_id,
        "name": scooter_name,
        "battery_level": scooter_battery_level
    }


# Get all scooters
@app.route('/api/electro_scooters', methods=['GET'])
def get_all_electro_scooters():
    scooters = ElectroScooter.query.all()
    return jsonify([template(scooter.id, scooter.name, scooter.battery_level) for scooter in scooters]), 200


# Get specific scooter by id
@app.route('/api/electro_scooters/<int:scooter_id>', methods=['GET'])
def get_electro_scooter_by_id(scooter_id):
    scooter = ElectroScooter.query.get(scooter_id)
    if scooter is None:
        return jsonify({"error": "Electro scooter not found"}), 404
    return jsonify(template(scooter.id, scooter.name, scooter.battery_level)), 200


# Create specific scooter by id
@app.route('/api/electro_scooters', methods=['POST'])
def add_electro_scooter():
    try:
        data = request.get_json()

        if app.config['ROLE'] != 'main':
            if 'token' not in data.keys():
                return jsonify({"error": "Backup server: Not allowed to change data."}), 403
            elif data['token'] != app.config['TOKEN']:
                return jsonify({"error": "Invalid token"}), 403
        else:
            data = data.copy()
            data['token'] = app.config['TOKEN']
            for follower in app.config['FOLLOWER_INSTANCES']:
                requests.post("http://" + follower['host'] + ":" + str(follower['port']) + "/api/electro_scooters", json=data)

        db.session.add(ElectroScooter(data['name'], data['battery_level']))
        db.session.commit()
        return jsonify({"message": "Electro scooter added successfully"}), 201
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid JSON"}), 400


# Update specific scooter by id
@app.route('/api/electro_scooters/<int:scooter_id>', methods=['PUT'])
def update_electro_scooter(scooter_id):
    try:
        data = request.get_json()

        if app.config['ROLE'] != 'main':
            if 'token' not in data.keys():
                return jsonify({"error": "Backup server: Not allowed to change data."}), 403
            elif data['token'] != app.config['TOKEN']:
                return jsonify({"error": "Invalid token"}), 403
        else:
            data = data.copy()
            data['token'] = app.config['TOKEN']
            for follower in app.config['FOLLOWER_INSTANCES']:
                requests.put("http://" + follower['host'] + ":" + str(follower['port']) + "/api/electro_scooters/" + str(scooter_id), json=data)

        electro_scooter = ElectroScooter.query.get(scooter_id)
        if electro_scooter is None:
            return jsonify({"error": "Electro scooter not found"}), 404

        electro_scooter.name = data['name']
        electro_scooter.battery_level = data['battery_level']
        db.session.commit()
        return jsonify({"message": "Electro scooter updated successfully"}), 200
    except:
        return jsonify({"error": "Invalid JSON"}), 400


# Delete specific scooter by id
@app.route('/api/electro_scooters/<int:scooter_id>', methods=['DELETE'])
def delete_electro_scooter(scooter_id):
    try:
        try:
            data = request.get_json()
        except:
            data = {}

        if app.config['ROLE'] != 'main':
            if 'token' not in data.keys():
                return jsonify({"error": "Backup server: Not allowed to change data."}), 403
            elif data['token'] != app.config['TOKEN']:
                return jsonify({"error": "Invalid token"}), 403
        else:
            data = data.copy()
            data['token'] = app.config['TOKEN']
            for follower in app.config['FOLLOWER_INSTANCES']:
                requests.delete("http://" + follower['host'] + ":" + str(follower['port']) + "/api/electro_scooters/" + str(scooter_id), json=data)

        electro_scooter = ElectroScooter.query.get(scooter_id)
        if electro_scooter is None:
            return jsonify({"error": "Electro scooter not found"}), 404

        db.session.delete(electro_scooter)
        db.session.commit()
        return jsonify({"message": "Electro scooter deleted successfully"}), 200
    except:
        return jsonify({"error": "Invalid JSON"}), 400
