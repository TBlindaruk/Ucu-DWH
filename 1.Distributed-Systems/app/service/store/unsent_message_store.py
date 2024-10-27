class UnsentMessageStoreSingleton:
    _instance = None
    _messages = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UnsentMessageStoreSingleton, cls).__new__(cls)
            cls._messages = {}
        return cls._instance

    def insert_into_replica_with_position(self, replica_name: str, position: int, message):
        if replica_name not in self._messages:
            self._messages[replica_name] = {}
        self._messages[replica_name][position] = message

    def get_by_replica_name(self, replica_name: str):
        if replica_name not in self._messages:
            return {}
        return self._messages[replica_name]

    def delete_by_replica_name_and_position(self, replica_name: str, position: int):
        del self._messages[replica_name][position]
