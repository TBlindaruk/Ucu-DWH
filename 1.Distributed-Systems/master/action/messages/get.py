from flask import jsonify

from service import MessageStoreSingleton

def get_list_action():
    return jsonify({ "data": MessageStoreSingleton().get_messages()}), 200

