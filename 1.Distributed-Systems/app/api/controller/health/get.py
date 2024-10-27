from flask import jsonify

from service.healthy.status_manager import secondaries_status

def get_health():
    return jsonify(secondaries_status), 200