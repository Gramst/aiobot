from .tdmsg_dataclass import Message, CallbackQuery

class InMessage:
    message : Message       = None
    callback: CallbackQuery = None

    def __init__(self, income_json: dict):
        keys = income_json.keys()
        if 'callback_query' in keys:
            self.callback = CallbackQuery.make_from_data(income_json.get('callback_query'))
            print(self.callback)
        if 'message' in keys:
            self.message = Message.make_from_data(income_json.get('message'))
            print(self.message)

    @property
    def not_empty(self) -> bool:
        if self.message or self.callback:
            return True
        return False
