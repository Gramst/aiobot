from typing import Union
from dataclasses import dataclass, field, asdict

from .t_messages import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
from .mix_methods import AIODoRequest

@dataclass
class sendMessage(AIODoRequest):
    #chat_id                 : int = field(init=False)
    text                    : str
    parse_mode              : str  = 'html'
    disable_web_page_preview: bool = False
    disable_notification    : bool = False
    reply_to_message_id     : int  = None
    reply_markup            : Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None


@dataclass
class sendPhoto(AIODoRequest):
    #chat_id             : int
    photo               : str
    caption             : str  = ''
    parse_mode          : str  = 'html'
    disable_notification: bool = False
    reply_to_message_id : int  = None
    reply_markup        : Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None

@dataclass
class sendAudio(AIODoRequest):
    #chat_id             : int
    audio               : str
    caption             : str  = ''
    parse_mode          : str  = 'html'
    duration            : int  = None
    performer           : str  = ''
    title               : str  = ''
    thumb               : str  = ''
    disable_notification: bool = False
    reply_to_message_id : int  = None
    reply_markup        : Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None

@dataclass
class sendVoice(AIODoRequest):
    #chat_id             : int
    voice               : str
    caption             : str  = ''
    parse_mode          : str  = 'html'
    duration            : int  = None
    disable_notification: bool = False
    reply_to_message_id : int  = None
    reply_markup        : Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply] = None

@dataclass
class answerCallbackQuery(AIODoRequest):
    callback_query_id : str
    text              : str = ''
    show_alert        : bool = False
    url               : str = ''
    cache_time        : int = 0

#@dataclass
#class sendChatAction(AIODoRequest):
#    action: Union['typing', 'upload_photo', 'record_video', 'upload_video', 'record_audio', 'upload_audio', for audio files, upload_document for general files, find_location for location data, record_video_note or upload_video_note for video notes.]