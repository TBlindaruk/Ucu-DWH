from flask import request

from config import GeneralConfig

class CreateMessageRequestData:

    @staticmethod
    def get_data():
        return request.json['data'] if 'data' in request.json else []

    @staticmethod
    def get_concern():
        return int(request.json['meta']['concern']) if 'meta' in request.json and 'concern' in request.json['meta'] else GeneralConfig.get_concern()

    @staticmethod
    def count_of_replica_concern():
        return CreateMessageRequestData.get_concern() - 1
