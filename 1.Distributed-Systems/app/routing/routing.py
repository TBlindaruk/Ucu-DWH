import threading

from flask import Flask

from api.controller.health import get as health_get
from api.controller.messages import get, create
from api.controller.messages.replica import create as replica_create, health
from config import AppModeConfing
from service.healthy.status_manager import heartbeat


class Routing:
    @staticmethod
    def init(app: Flask):
        app.add_url_rule('/messages', 'message_get', get.get_list_action, methods=['GET'])

        if AppModeConfing().is_master():
            app.add_url_rule('/messages', 'message_create', create.create_action, methods=['POST'])
            app.add_url_rule('/health', 'health_get', health_get.get_health, methods=['GET'])

        if AppModeConfing().is_replica():
            app.add_url_rule('/internal/messages/<int:position>', 'internal_message_create', replica_create.create_action, methods=['POST'])
            app.add_url_rule('/internal/health', 'internal_health_get', health.get_health, methods=['GET'])

class Heartbeat:
    @staticmethod
    def init():
        heartbeat_thread = threading.Thread(target=heartbeat)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()
