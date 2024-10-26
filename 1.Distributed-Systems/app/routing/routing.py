from flask import Flask

from api.controller.messages import get, create, health
from api.controller.messages.replica import create as replica_create
from config import AppModeConfing

class Routing:
    @staticmethod
    def init(app: Flask):
        app.add_url_rule('/messages', 'message_get', get.get_list_action, methods=['GET'])
        app.add_url_rule('/healthy', 'health_get', health.get_health, methods=['GET'])

        if AppModeConfing().is_master():
            app.add_url_rule('/messages', 'message_create', create.create_action, methods=['POST'])

        if AppModeConfing().is_replica():
            app.add_url_rule('/internal/messages/<int:position>', 'internal_message_create', replica_create.create_action, methods=['POST'])
