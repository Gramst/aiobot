from dataclasses import dataclass, field
from typing import List, Union
import asyncio

from .telegramclasses.t_messages import Message, CallbackQuery
from .telegramclasses.t_methods import sendMessage, sendPhoto, sendAudio, sendVoice
from .telegramclasses.t_messages import InlineKeyboardMarkup, InlineKeyboardButton

from ..database import ReplyChain

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
        else:
            print(f'message not ok\ndict {income_json}')

class OutMessage:
    base_url            : str
    db                  : ReplyChain
    file_id             : str
    from_id             : int
    from_message_id     : int
    text                : str
    promt               : str
    split               : str
    method              : Union[sendMessage, sendPhoto, sendAudio, sendVoice]
    reply_to_message_id : int        = None
    reply_messages_ids  : List[list] = []

    def __init__(self, **kwargs):
        self.file_id = kwargs.get('file_id')
        self.from_id = kwargs.get('from_id')
        self.text    = kwargs.get('text')
        self.promt   = kwargs.get('promt', '')
        self.split   = kwargs.get('split', ' 🗣 ')


    def gen_message(self, method: Union[sendMessage, sendPhoto, sendAudio, sendVoice]):
        if isinstance(method, sendMessage):
            if self.text:
                self.method = sendMessage(text = self.promt + self.text)
        if isinstance(method, sendPhoto):
            if self.file_id:
                if self.text:
                    self.method = sendPhoto(photo   = self.file_id,
                                            caption = self.text)
                else:
                    button = InlineKeyboardButton(  text = self.promt,
                                                    callback_data='asd')
                    self.method = sendPhoto(photo        = self.file_id,
                                            reply_markup = InlineKeyboardMarkup(inline_keyboard = [button]))
        if isinstance(method, sendVoice):
            if self.file_id:
                self.method = sendVoice(voice = self.file_id)


    def __lshift__(self, other: InMessage) -> None:
        if not isinstance(other, InMessage):
            return
        self.from_id = other.message.from_u.id
        self.from_message_id = other.message.message_id
        if other.message.reply_to_message:
            self.reply_to_message_id = other.message.reply_to_message.message_id
        if other.message.text:
            text = other.message.text
            if self.promt:
                text = self.promt + self.split + text
            self.method  = sendMessage(text)
        if other.message.photo:
            button = InlineKeyboardButton(  text = self.promt,
                                            callback_data='asd')
            self.method = sendPhoto(other.message.photo[0].file_id,
                                    caption = other.message.caption,
                                    reply_markup = InlineKeyboardMarkup([[button]]))
        if other.message.audio:
            self.method = sendAudio(other.message.audio.file_id,
                                    caption = other.message.audio.file_id)
        if other.message.voice:
            self.method = sendVoice(other.message.voice.file_id,
                                    caption = other.message.voice.file_id)

    async def get_reply_block(self):
        print(f'reply to {self.reply_to_message_id}')
        if self.reply_to_message_id:
            self.reply_messages_ids = await self.db.get_reply(self.reply_to_message_id)
        print(f'replys {self.reply_messages_ids}')

    def _get_message_id_for_reply(self, chat_id: int) -> int:
        if self.reply_messages_ids:
            _ = [i[3] for i in self.reply_messages_ids if i[2] == chat_id]
            if _:
                return _[0]
        return None

    def set_destination(self, dest: List[int]):
        self.destinations = dest

    async def send_to_server(self):
        _ = [self._send_to_server(i) for i in self.destinations]
        await asyncio.wait(_)

    async def _send_to_server(self, chat_id: int):
        if self.reply_messages_ids:
            self.method.reply_to_message_id = self._get_message_id_for_reply(chat_id)
        res = ResponseMessage(await self.method.do_request(self.base_url, chat_id))
        if res.ok and (self.from_id and self.from_message_id):
            print(f'adding data to reply {self.from_id} {res.result.message_id}')
            await self.db.add_data(
                    self.from_id,
                    self.from_message_id,
                    res.result.chat.id,
                    res.result.message_id,
                    res.result.date
                    )
