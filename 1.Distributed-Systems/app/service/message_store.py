from asyncio import sleep

from time import sleep


class MessageStoreSingleton:
    _instance = None
    _messages = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MessageStoreSingleton, cls).__new__(cls)
            cls._messages = []
        return cls._instance

    def append(self, message):
        self._messages.append(message)

        return len(self._messages) - 1

    def insert_with_rewrite(self, position: int, message):
        while position >= len(self._messages):
            self._messages.append(None)
        self._messages[position] = message

    def get_messages(self):
        return self._messages