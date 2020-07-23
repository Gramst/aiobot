from typing import Union
from dataclasses import dataclass, field, asdict

from .t_messages import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
from .mix_methods import AIODoRequest

@dataclass
class baseChatSettings:
    chat_id                 : int
    parse_mode              : str  = 'html'
    disable_web_page_preview: bool = False
    disable_notification    : bool = False
    

    def get(self) -> dict:
        res: dict = asdict(self)
        if self.parse_mode not in ['html', 'markdown']:
            res.pop('parse_mode')
        if not self.disable_web_page_preview:
            res.pop('disable_web_page_preview')
        if not self.disable_notification:
            res.pop('disable_notification')
        return(res)

@dataclass
class sendMessage(AIODoRequest):
    chat_id                 : int
    text                    : str
    parse_mode              : str  = 'html'
    disable_web_page_preview: bool = False
    disable_notification    : bool = False
    reply_to_message_id     : int  = None
    reply_markup            : Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None


@dataclass
class sendPhoto(AIODoRequest):
    chat_id                 : int
    photo                   : str
    caption                 : str
    parse_mode              : str  = 'html'
    disable_web_page_preview: bool = False
    disable_notification    : bool = False
    reply_to_message_id     : int = None
    reply_markup : Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None
