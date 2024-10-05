from flask import Flask

from action.messages import create, get

class Routing:
    @staticmethod
    def init(app: Flask):
        app.add_url_rule('/messages', 'create', create.create_action, methods=['POST'])
        app.add_url_rule('/messages', 'get', get.get_list_action, methods=['GET'])