from typing import Union
from dataclasses import dataclass, field

from .t_messages import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
from .mix_methods import AIODoRequest

@dataclass
class baseChatSettings:
    chat_id                 : int
    parse_mode              : str  = 'html'
    disable_web_page_preview: bool = False
    disable_notification    : bool = False

    def get(self) -> dict:
        res: dict = self.asdict()
        if self.parse_mode not in ['html', 'markdown']:
            res.pop('parse_mode')
        if not self.disable_web_page_preview:
            res.pop('disable_web_page_preview')
        if not self.disable_notification:
            res.pop('disable_notification')
        return(res)

@dataclass
class sendMessage(AIODoRequest):
    text                    : str
    chat_settings           : baseChatSettings = None
    reply_to_message_id     : int              = None
    reply_markup            : Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None


    def get_data(self) -> dict:
        res = self.chat_settings.get()
        res['text'] = self.text
        if self.reply_to_message_id:
            res['reply_to_message_id'] = self.reply_to_message_id
        if self.reply_markup:
            res['reply_markup'] = self.reply_markup
        return res


