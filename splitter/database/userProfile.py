from .mix_db import gen_random_nick

class UserFlags:

    def __init__(self):
        self.ban    : bool = False
        self.active : bool = True

class BaseData:

    def __init__(self):
        self.chat_id: int
        self.flags  : UserFlags = UserFlags()

class User(BaseData):
    
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.nick    = gen_random_nick

    def update(self):
        pass