class MessageStoreSingleton:
    _instance = None
    _messages = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MessageStoreSingleton, cls).__new__(cls)
            cls._messages = []
        return cls._instance

    def add_message(self, message):
        self._messages.append(message)

    def get_messages(self):
        return self._messages