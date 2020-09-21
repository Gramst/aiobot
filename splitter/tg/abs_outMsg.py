from typing import List, Union, Callable


from .telegramclasses.t_messages import InlineKeyboardMarkup, InlineKeyboardButton
from .. import Splitter
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

class Text(FormatHTML):
    original_value: str
    tags          : list

    def __init__(self):
        self.original_value = ''
        self.tags = []

    def clear_tags(self):
        self.tags.clear()

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
        if res:
            for i in self.tags:
                res = self.add_tag(res, i)
        return res

    @property
    def result(self) -> str:
        return f'{self}'

    def __lshift__(self, other: str):
        if isinstance(other, str):
            self.original_value = other
        else:
            try:
                self.original_value = str(other)
            except Exception as e:
                print(e)

class Reply:
    raw_reply_to: int
    reply_block : list

    async def set_async(self, reply_to: int) -> None:
        self.raw_reply_to = reply_to
        db = Splitter().message_database
        if self.raw_reply_to:
            self.reply_block = await db.get_reply(self.raw_reply_to)

    def get_message_id_for_reply(self, chat_id: int) -> int:
        if self.reply_block:
            _ = [i[3] for i in self.reply_block if i[2] == chat_id]
            if _:
                return _[0]
        return None

class TextPreSet:
    MASTER  : int = 0
    SLAVE   : int = 1
    OTHER   : int = 2
    TEXT    : int = 3
    FILE_ID : int = 4
    CUSTOM  : int = 5

    def __init__(self, value: str, custom: str = ''):
        self.text_format_list : List[Text] = [Text(), Text(), Text(), Text(), Text(), Text()]
        self.forming_test_string = value
        self.text_format_list[self.CUSTOM] << custom

    def make_result(self) -> str:
        res = self.forming_test_string.format(  master  = self.text_format_list[self.MASTER].result,
                                                slave   = self.text_format_list[self.SLAVE].result,
                                                other   = self.text_format_list[self.OTHER].result,
                                                text    = self.text_format_list[self.TEXT].result,
                                                file_id = self.text_format_list[self.TEXT].result,
                                                custom  = self.text_format_list[self.CUSTOM].result)
        res.strip()
        return res

    def set_values(self, out_msg: "OutMessage", current_user: User):
        self.text_format_list[self.MASTER]     << out_msg.master.nick
        if out_msg.slave:
            self.text_format_list[self.SLAVE]  << out_msg.slave.nick
        self.text_format_list[self.TEXT]       << out_msg.text
        self.text_format_list[self.OTHER]      << current_user.nick
        self.text_format_list[self.FILE_ID]    << out_msg.file_id

class TextHandler:

    def __init__(self, mm_val: TextPreSet, ms_val: TextPreSet, mo_val: TextPreSet):
        self.mm    : TextPreSet = mm_val
        self.ms    : TextPreSet = ms_val
        self.mo    : TextPreSet = mo_val

    def process(self, out_msg: "OutMessage", current_user: User) -> str:
        if out_msg.master == current_user:
            self.mm.set_values(out_msg, current_user)
            return self.mm.make_result()
        elif out_msg.slave and out_msg.slave == current_user:
            self.ms.set_values(out_msg, current_user)
            return self.ms.make_result()
        else:
            self.mo.set_values(out_msg, current_user)
            return self.mo.make_result()

class InlineKeyboard:

    def __init__(self):
        self.keys = list()

    def add_key(self, key: InlineKeyboardButton) -> None:
        self.keys.append([key])

    def add_keys(self, keys: List[InlineKeyboardButton]) -> None:
        self.keys.append(keys)

    def make_keyboard(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(self.keys)

    @staticmethod
    def make_key(text: str, callback_data: str = '') -> InlineKeyboardButton:
        return InlineKeyboardButton(text = text, callback_data=callback_data)

class MessageInBotNotification:

    def __init__(self):
        self._regular: bool = True
        self._social : bool = False
        self._system : bool = False
        self._reply  : bool = False

    def set_notify_to_regular(self):
        self._regular = True
        self._social = False
        self._system = False

    def set_notify_to_social(self):
        self._regular = False
        self._social = True
        self._system = False

    def set_notify_to_system(self):
        self._regular = False
        self._social = False
        self._system = True

    def get_notification_flag(self, out_msg: "OutMessage", user: User):
        if self._regular:
            return user.msg_flags.normal
        if self._social:
            return user.msg_flags.social
        if self._system:
            return user.msg_flags.system

class OutMessage:
    master     : User
    slave      : User
    method_name: 'NoName'

    def __init__(self, text_handler: TextHandler):
        self.file_id             : str   = None
        self.from_id             : int   = None
        self.from_message_id     : int   = None
        self.text                : str   = ''
        self.splitter            : str   = ' : '
        self.reply               : Reply = Reply()
        self.destinations        : List[User] = []
        self.f_no_reply          : bool = False
        self.notify_msg          = MessageInBotNotification()
        #self.method_name         : str  = ''
        self.text_handler        : TextHandler = text_handler
        self.inline_keyboard     = InlineKeyboard()

    def gen_data_server_request(self) -> dict:
        # yeld
        raise NotImplementedError

class TextMessage(OutMessage):
    method_name: str = 'sendMessage'

    def gen_data_server_request(self) -> dict:
        for user in self.destinations:
            user: User = user
            result = dict()
            result['text'] = self.text_handler.process(self, user)
            result['chat_id']    = user.chat_id
            result['parse_mode'] = 'html'
            result['notification'] = self.notify_msg.get_notification_flag(self, user)
            if not self.f_no_reply:
                result['reply_to_message_id'] = self.reply.get_message_id_for_reply(user.chat_id)
            yield result

class PhotoMessage(OutMessage):
    method_name: str = 'sendPhoto'

    def gen_data_server_request(self) -> dict:
        for user in self.destinations:
            user: User = user
            result = dict()
            result['caption']    = self.text_handler.process(self, user)
            result['chat_id']    = user.chat_id
            result['file_id']    = self.file_id
            result['parse_mode'] = 'html'
            if not self.f_no_reply:
                result['reply_to_message_id'] = self.reply.get_message_id_for_reply(user.chat_id)
            yield result