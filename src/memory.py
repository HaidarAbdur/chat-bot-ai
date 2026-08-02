class ConversationMemory:
    def __init__(self):
        self._messages = []
    
    def add_message(self, role, content):
        self._messages.append({"role": role, "content": content})

    def get_history(self):
        return list(self._messages) 

    def clear(self):
        self._messages = []

