from flask import Flask

from action.messages import create, get
from action.messages.replica import create as replica_create
from config import AppModeConfing

class Routing:
    @staticmethod
    def init(app: Flask):
        app.add_url_rule('/messages', 'get', get.get_list_action, methods=['GET'])

        if AppModeConfing().is_master():
            app.add_url_rule('/messages', 'create', create.create_action, methods=['POST'])

        if AppModeConfing().is_replica():
            app.add_url_rule('/internal/messages', 'create_init', replica_create.create_action, methods=['POST'])

