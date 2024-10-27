def insert_or_replace(lst, position, value):
    if position < len(lst):
        lst[position] = value
    else:
        lst.append(value)

class MessageStoreSingleton:
    _instance = None
    _messages = []
    _un_showed_messages = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MessageStoreSingleton, cls).__new__(cls)
            cls._messages = []
        return cls._instance

    def append(self, message):
        self._messages.append(message)

        return len(self._messages) - 1

    def insert_with_order(self, position: int, message):
        if position > len(self._messages):
            self._un_showed_messages[position] = message
            return

        insert_or_replace(self._messages, position, message)

        next_position = position + 1
        if next_position in self._un_showed_messages and self._un_showed_messages[next_position] is not None:
            self.insert_with_order(next_position, self._un_showed_messages[next_position])
            del self._un_showed_messages[next_position]

    def get_messages(self):
        return self._messages