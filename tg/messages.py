from dataclasses import dataclass, field
from typing import List, Union
import asyncio

from .telegramclasses.t_messages import Message, CallbackQuery
from .telegramclasses.t_methods import sendMessage, baseChatSettings

class InMessage:
    message : Message       = None
    callback: CallbackQuery = None

    def __init__(self, income_json: dict):
        keys = income_json.keys()
        if 'callback_query' in keys:
            self.callback = CallbackQuery.make_from_data(income_json.get('callback_query'))
            self.message = self.callback.message
            print(self.callback)
        elif 'message' in keys:
            self.message = Message.make_from_data(income_json.get('message'))
            print(self.message)

    @property
    def not_empty(self) -> bool:
        if self.message or self.callback:
            return True
        return False

# @dataclass(init=False)
class OutMessage:
    # method          : Union[sendMessage, ]
    # from_id         : int
    # from_message_id : int
    # text            : str
    # file_id         : List[str]

    def __init__(self, data):
        self.sm = sendMessage
        self.sm.API_URL = data

    def __lshift__(self, other: InMessage) -> None:
        if not isinstance(other, InMessage):
            return

        self.from_id = other.message.from_u.id
        self.from_message_id = other.message.message_id
        if other.message.text:
            self.method  = sendMessage(other.message.text, baseChatSettings(other.message.from_u.id))
        # if other.message.photo:
        #     self.method  = sendMessage
        #     self.text    = other.message.caption
        #     self.file_id = [i.file_id for i in other.message.photo]
        # if other.message.audio:
        #     self.method  = sendMessage
        #     self.text    = other.message.caption
        #     self.file_id = [other.message.audio.file_id]
        # if other.message.sticker:
        #     self.method  = sendMessage
        #     self.file_id = other.message.sticker.file_id

    async def send_to(self):
        res = await self.method.do_request()
        return res
        

            
