from flask import jsonify

def get_list_action(messages):
    return jsonify({ "data": messages}), 200

