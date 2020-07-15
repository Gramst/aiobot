from dataclasses import dataclass
from typing import Union

from messages.typestgmessages import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply

@dataclass(init=False)
class sendMessage:
    chat_id                 : int 
    text                    : str 
    parse_mode              : str 
    disable_web_page_preview: bool
    disable_notification    : bool
    reply_to_message_id     : int
    reply_markup            : Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]