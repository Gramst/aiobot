from dataclasses import dataclass, field
from typing import List, Union
import asyncio

from .telegramclasses.t_messages import Message, CallbackQuery
from .telegramclasses.t_methods import sendMessage, sendPhoto

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

    @property
    def not_empty(self) -> bool:
        if self.message or self.callback:
            return True
        return False

class ResponseMessage:
    from_id        : int
    from_message_id: int
    ok             : bool    = False
    result         : Message = None

    def __init__(self, income_json: dict):
        self.ok = income_json.get('ok', False)
        if self.ok:
            self.result = Message.make_from_data(income_json.get('result'))

class OutMessage:

    def __lshift__(self, other: InMessage) -> None:
        if not isinstance(other, InMessage):
            return
        self.from_id = other.message.from_u.id
        self.from_message_id = other.message.message_id
        if other.message.text:
            self.method  = sendMessage( other.message.from_u.id,
                                        other.message.text)
        if other.message.photo:
            self.method  = sendPhoto(   other.message.from_u.id,
                                        other.message.photo[0].file_id,
                                        other.message.caption)
        # if other.message.audio:
        #     self.method  = sendMessage
        #     self.text    = other.message.caption
        #     self.file_id = [other.message.audio.file_id]
        # if other.message.sticker:
        #     self.method  = sendMessage
        #     self.file_id = other.message.sticker.file_id

    async def send_to_server(self, base_url: str) -> ResponseMessage:
        res = ResponseMessage(await self.method.do_request(base_url))
        if res.ok:
            res.from_id         = self.from_id
            res.from_message_id = self.from_message_id
            return res
        return None
