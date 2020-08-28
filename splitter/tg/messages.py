from dataclasses import dataclass, field
from typing import List, Union
import asyncio
from time import time

from .telegramclasses.t_messages import Message, CallbackQuery
from .telegramclasses.t_methods import sendMessage, sendPhoto, sendAudio, sendVoice
from .telegramclasses.t_messages import InlineKeyboardMarkup, InlineKeyboardButton

from ..database import ReplyChain
from ..database import User
class FormatHTML:
    BOLD          : str = 'b'
    ITALIC        : str = 'i'
    UNDERLINE     : str = 'u'
    STRIKETHROUGHT: str = 's'
    CODE          : str = 'code'

    def add_tag(self, text: str, tagsymbol: str = None) -> str:
        if not tagsymbol:
            return text
        return f'<{tagsymbol}>' + text + f'</{tagsymbol}>'

    def replace_s(self, text:str) -> str:
        dict_to_replace = {
            '&' : '&amp;',
            '<' : '&lt;',
            '>' : '&gt;',
        }
        for i in dict_to_replace:
            text = text.replace(i, dict_to_replace[i])
        return text

class OutText(FormatHTML):
    original_value: str
    tags          : list

    def __init__(self):
        self.original_value = ''
        self.tags = []

    def as_bold(self) -> None:
        self.tags.append(self.BOLD)

    def as_italic(self) -> None:
        self.tags.append(self.ITALIC)

    def as_underline(self) -> None:
        self.tags.append(self.UNDERLINE)

    def as_strikethrought(self) -> None:
        self.tags.append(self.STRIKETHROUGHT)

    def as_code(self) -> None:
        self.tags.append(self.CODE)

    def __repr__(self):
        res = self.replace_s(self.original_value)
        for i in self.tags:
            res = self.add_tag(res, i)
        return res

    def __lshift__(self, other: str):
        if isinstance(other, str):
            self.original_value = other
        else:
            try:
                self.original_value = str(other)
            except Exception as e:
                print(e)


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

@dataclass
class MessageNotificationTypes:
    __normal: bool = True
    __social: bool = False
    __system: bool = False

    def set_notify_to_normal(self):
        self.__normal = True
        self.__social = False
        self.__system = False

    def set_notify_to_social(self):
        self.__normal = False
        self.__social = True
        self.__system = False

    def set_notify_to_system(self):
        self.__normal = False
        self.__social = False
        self.__system = True

    @property
    def notify_type_normal(self):
        return self.__normal

    @property
    def notify_type_social(self):
        return self.__social

    @property
    def notify_type_system(self):
        return self.__social


class OutMessage(FormatHTML, MessageNotificationTypes):
    base_url            : str
    db                  : ReplyChain
    file_id             : str
    from_id             : int = None
    from_message_id     : int = None
    text_obj            : OutText
    promt_obj           : OutText
    split_obj           : OutText
    method              : Union[sendMessage, sendPhoto, sendAudio, sendVoice]
    reply_to_message_id : int        = None
    reply_messages_ids  : List[list] = []
    destinations        : List[User]

    def __init__(self, **kwargs):
        self.text_obj = OutText()
        self.promt_obj= OutText()
        self.split_obj= OutText()
        self.destinations = []
        self.file_id  = kwargs.get('file_id')
        self.from_id  = kwargs.get('from_id')
        self.text     = kwargs.get('text')
        self.promt    = kwargs.get('promt', '')
        self.split    = kwargs.get('split', ' 🗣 ')

    @property
    def text(self):
        return f'{self.text_obj}'

    @text.setter
    def text(self, value: str):
        self.text_obj << value

    @property
    def promt(self):
        return f'{self.promt_obj}'

    @promt.setter
    def promt(self, value: str):
        self.promt_obj << value

    @property
    def split(self):
        return f'{self.split_obj}'

    @split.setter
    def split(self, value: str):
        self.split_obj << value

    def as_text(self) -> None:
        if self.text:
            self.method = sendMessage(self.promt + self.text)

    def __lshift__(self, other: InMessage) -> None:
        if not isinstance(other, InMessage):
            return
        self.from_id = other.message.from_u.id
        self.from_message_id = other.message.message_id
        if other.message.reply_to_message:
            self.reply_to_message_id = other.message.reply_to_message.message_id
        if other.message.text:
            self.text = other.message.text
            if self.promt:
                text = self.promt + self.split + self.text
            self.method  = sendMessage(text)
        if other.message.photo:
            button = InlineKeyboardButton(  text = self.promt_obj.original_value,
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

    def add_destination(self, to_user: Union[User, int]):
        if isinstance(to_user, User):
            self.destinations.append(to_user)
        elif isinstance(to_user, int):
            self.destinations.append(User(to_user))


    async def send_to_server(self):
        if self.from_id and self.from_message_id:
            await self.db.add_data(self.from_id, self.from_message_id, self.from_id, self.from_message_id, int(time()))
        _ = []
        if self.notify_type_normal:
            if self.reply_messages_ids:
                for user in self.destinations:
                    if user.chat_id != self.reply_messages_ids[0][0]:
                        _.append(self._send_to_server(user.chat_id, user.msg_flags.normal))
                    _.append(self._send_to_server(user.chat_id, user.msg_flags.reply))
            else:
                _ = [self._send_to_server(i.chat_id, i.msg_flags.normal) for i in self.destinations]
        elif self.notify_type_social:
            _ = [self._send_to_server(i.chat_id, i.msg_flags.social) for i in self.destinations]
        elif self.notify_type_system:
            _ = [self._send_to_server(i.chat_id, i.msg_flags.system) for i in self.destinations]
        else:
            _ = [self._send_to_server(i.chat_id) for i in self.destinations]
        await asyncio.wait(_)

    async def _send_to_server(self, chat_id: int, notification: bool = True):
        if not notification:
            self.method.disable_notification = True
        if self.reply_messages_ids:
            self.method.reply_to_message_id = self._get_message_id_for_reply(chat_id)
        res = ResponseMessage(await self.method.do_request(self.base_url, chat_id))
        if res.ok and (self.from_id and self.from_message_id):
            print(f'adding data to reply {self.from_id} {self.from_message_id} {res.result.chat.id} {res.result.message_id}')
            await self.db.add_data(
                    self.from_id,
                    self.from_message_id,
                    res.result.chat.id,
                    res.result.message_id,
                    res.result.date
                    )
