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
