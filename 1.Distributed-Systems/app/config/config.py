import os

class AppModeConfing:
    MODE_MASTER = 'app'
    MODE_REPLICA = 'replica'

    def __get_app_mode(self):
        return os.getenv('APP_MODE') or self.MODE_MASTER

    def is_master(self):
        return self.__get_app_mode() == self.MODE_MASTER

    def is_replica(self):
        return self.__get_app_mode() == self.MODE_REPLICA

class GeneralConfig:
    @staticmethod
    def get_concern():
        return int(os.getenv('CONCERN'))

    @staticmethod
    def get_replicas():
        return {key: value for key, value in os.environ.items() if key.startswith("REPLICA_HOST")}
