from typing import List
from dataclasses import dataclass, field

from .datamix import FromIncomeData

@dataclass
class User(FromIncomeData):
    KEYS = ['id', 'is_bot', 'first_name', 'last_name', 'username', 'language_code', 'can_join_groups',
    'can_read_all_group_messages', 'supports_inline_queries']
    id           : int
    is_bot       : bool
    first_name   : str
    last_name    : str
    username     : str
    language_code: str
    can_join_groups            : bool
    can_read_all_group_messages: bool
    supports_inline_queries    : bool

@dataclass
class ChatPhoto(FromIncomeData):
    KEYS = ['small_file_id', 'small_file_unique_id', 'big_file_id', 'big_file_unique_id']
    small_file_id       : str
    small_file_unique_id: str
    big_file_id         : str
    big_file_unique_id  : str

@dataclass
class ChatPermissions(FromIncomeData):
    KEYS = ['can_send_messages', 'can_send_media_messages', 'can_send_polls', 'can_send_other_messages',
    'can_add_web_page_previews', 'can_change_info', 'can_invite_users', 'can_pin_messages']
    can_send_messages: bool
    can_send_media_messages: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_previews: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool

@dataclass
class Chat(FromIncomeData):
    KEYS = ['id', 'type', 'title', 'username', 'first_name', 'last_name', 'photo',
    'description', 'invite_link', 'pinned_message', 'permissions', 'slow_mode_delay',
    'sticker_set_name', 'can_set_sticker_set']
    id: int
    type: str
    title: str
    username: str
    first_name: str
    last_name: str
    __photo : dict = field(repr=False)
    photo: 'ChatPhoto' = field(init=False)
    description: str
    invite_link: str
    __pinned_message: dict = field(repr=False)
    pinned_message: 'Message' = field(init=False)
    __permissions: dict = field(repr=False)
    permissions: 'ChatPermissions'  = field(init=False)
    slow_mode_delay: int
    sticker_set_name: str
    can_set_sticker_set: bool

    def __post_init__(self):
        self.photo: 'ChatPhoto' = ChatPhoto.make_from_data(self.__photo)
        self.pinned_message: 'Message' = Message.make_from_data(self.__pinned_message)
        self.permissions: 'ChatPermissions' = ChatPermissions.make_from_data(self.__permissions)

@dataclass
class MessageEntity(FromIncomeData):
    KEYS = ['type', 'offset', 'length', 'url', 'user', 'language']
    type: str
    offset: int
    length: int
    url: str
    __user: dict = field(repr=False)
    user: 'User' = field(init=False)
    language: str

    def __post_init__(self):
        self.user: 'User' = User.make_from_data(self.__user)

@dataclass
class PhotoSize(FromIncomeData):
    KEYS = ['file_id', 'file_unique_id', 'width', 'height', 'file_size']
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: int

#TODO data reused class

@dataclass
class Animation(FromIncomeData):
    KEYS = ['file_id', 'file_unique_id', 'width', 'height', 'duration', 'thumb', 
    'file_name', 'mime_type', 'file_size']
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    __thumb: dict = field(repr=False)
    thumb: 'PhotoSize' = field(init=False)
    file_name: str
    mime_type: str
    file_size: int
    
    def __post_init__(self):
        self.thumb: 'PhotoSize' = PhotoSize.make_from_data(self.__thumb)

@dataclass
class Audio(FromIncomeData):
    KEYS = ['file_id', 'file_unique_id', 'duration', 'performer', 'title', 'mime_type',
    'file_size', 'thumb']
    file_id: str
    file_unique_id: str
    duration: int
    performer: str
    title: str
    mime_type: str
    file_size: int
    __thumb: dict = field(repr=False)
    thumb: 'PhotoSize' = field(init=False)

    def __post_init__(self):
        self.thumb: 'PhotoSize' = PhotoSize.make_from_data(self.__thumb)

@dataclass
class Document(FromIncomeData):
    KEYS = ['file_id', 'file_unique_id', 'thumb', 'file_name', 'mime_type', 'file_size']
    file_id: str
    file_unique_id: str
    __thumb: dict = field(repr=False)
    thumb: 'PhotoSize' = field(init=False)
    file_name: str
    mime_type: str
    file_size: int

    def __post_init__(self):
        self.thumb: 'PhotoSize' = PhotoSize.make_from_data(self.__thumb)

@dataclass
class MaskPosition(FromIncomeData):
    KEYS = ['point', 'x_shift', 'y_shift', 'scale']
    point: str
    x_shift: float
    y_shift: float
    scale: float

@dataclass
class Sticker(FromIncomeData):
    KEYS = ['file_id', 'file_unique_id', 'width', 'height', 'is_animated', 'thumb', 
    'emoji', 'set_name', 'mask_position', 'file_size']
    file_id: str
    file_unique_id: str
    width: int
    height: int
    is_animated: bool
    __thumb: dict = field(repr=False)
    thumb: 'PhotoSize' = field(init=False)
    emoji: str
    set_name: str
    __mask_position: dict = field(repr=False)
    mask_position: 'MaskPosition' = field(init=False)
    file_size: int

    def __post_init__(self):
        self.thumb: 'PhotoSize' = PhotoSize.make_from_data(self.__thumb)
        self.mask_position: 'MaskPosition' = MaskPosition.make_from_data(self.__mask_position)

@dataclass
class Video(FromIncomeData):
    KEYS = ['file_id', 'file_unique_id', 'width', 'height', 'duration', 'thumb', 'mime_type', 'file_size']
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    __thumb: dict = field(repr=False)
    thumb: 'PhotoSize' = field(init=False)
    mime_type: str
    file_size: int

    def __post_init__(self):
        self.thumb: 'PhotoSize' = PhotoSize.make_from_data(self.__thumb)

@dataclass
class VideoNote(FromIncomeData):
    KEYS = ['file_id', 'file_unique_id', 'length', 'duration', 'thumb', 'file_size']
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    __thumb: dict = field(repr=False)
    thumb: 'PhotoSize' = field(init=False)
    file_size: int

    def __post_init__(self):
        self.thumb: 'PhotoSize' = PhotoSize.make_from_data(self.__thumb)

@dataclass
class Voice(FromIncomeData):
    KEYS = ['file_id', 'file_unique_id', 'duration', 'mime_type', 'file_size']
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: str
    file_size: int

@dataclass
class Contact(FromIncomeData):
    KEYS = ['phone_number', 'first_name', 'last_name', 'user_id', 'vcard']
    phone_number: str
    first_name: str
    last_name: str
    user_id: int
    vcard: str

@dataclass
class Dice(FromIncomeData):
    KEYS = ['emoji', 'value']
    emoji: str
    value: int

@dataclass
class Game(FromIncomeData):
    KEYS = ['title', 'description', 'photo', 'text', 'text_entities', 'animation']
    title: str
    description: str
    __photo: list = field(repr=False)
    photo: List[PhotoSize] = field(init=False)
    text: str
    __text_entities: list = field(repr=False)
    text_entities: List[MessageEntity] = field(init=False)
    __animation: list = field(repr=False)
    animation: 'Animation' = field(init=False)

    def __post_init__(self):
        self.photo: List[PhotoSize] = PhotoSize.make_list_from_data(self.__photo)
        self.text_entities: List[MessageEntity] = MessageEntity.make_list_from_data(self.__text_entities)
        self.animation: 'Animation' = Animation.make_from_data(self.__animation)

@dataclass
class PollOption(FromIncomeData):
    KEYS = ['text','voter_count']
    text: str
    voter_count: int

@dataclass
class Poll(FromIncomeData):
    KEYS = ['id', 'question', 'options', 'total_voter_count', 'is_closed', 'is_anonymous',
    'type', 'allows_multiple_answers', 'correct_option_id', 'explanation', 'explanation_entities',
    'open_period', 'close_date']
    id                     : str
    question               : str
    __options              : list = field(repr=False)
    options                : List[PollOption] = field(init=False)
    total_voter_count      : int
    is_closed              : bool
    is_anonymous           : bool
    type                   : str
    allows_multiple_answers: bool
    correct_option_id      : int
    explanation            : str
    __explanation_entities : list = field(repr=False)
    explanation_entities   : List[MessageEntity] = field(init=False)
    open_period            : int
    close_date             : int

    def __post_init__(self):
        self.options: List[PollOption] = PollOption.make_list_from_data(self.__options)
        self.explanation_entities: List[MessageEntity] = MessageEntity.make_list_from_data(self.__explanation_entities)

@dataclass
class Location(FromIncomeData):
    KEYS = ['longitude', 'latitude']
    longitude: float
    latitude: float

@dataclass
class Venue(FromIncomeData):
    KEYS = ['location', 'title', 'address', 'foursquare_id', 'foursquare_type']
    __location     : dict       = field(repr=False)
    location       : 'Location' = field(init=False)
    title          : str
    address        : str
    foursquare_id  : str
    foursquare_type: str

    def __post_init__(self):
        location: 'Location' = Location.make_from_data(self.__location)

@dataclass
class SuccessfulPayment(FromIncomeData):
    pass

@dataclass
class PassportData(FromIncomeData):
    pass

@dataclass
class LoginUrl(FromIncomeData):
    KEYS = ['url', 'forward_text', 'bot_username', 'request_write_access']
    url: str
    forward_text: str
    bot_username: str
    request_write_access: bool

@dataclass
class InlineKeyboardButton(FromIncomeData):
    KEYS = ['text', 'url', 'login_url', 'callback_data', 'switch_inline_query',
    'switch_inline_query_current_chat', 'pay']
    text               : str 
    url                : str 
    __login_url        : dict = field(repr=False)
    login_url          : 'LoginUrl' = field(init=False)
    callback_data      : str
    switch_inline_query: str
    switch_inline_query_current_chat: str 
    #TODO callback_game	CallbackGame
    pay                : bool

    def __post_init__(self):
        self.login_url: 'LoginUrl' = LoginUrl.make_from_data(self.__login_url)

@dataclass
class InlineKeyboardMarkup(FromIncomeData):
    __inline_keyboard: list = field(repr=False)
    inline_keyboard  : list = field(init=False)

    def __post_init__(self):
        self.inline_keyboard = [InlineKeyboardButton.make_list_from_data(i) for i in self.__inline_keyboard]

@dataclass
class Message(FromIncomeData):  
    KEYS = ['message_id', 'from', 'date', 'chat', 'forward_from', 'forward_from_chat',
    'forward_from_message_id', 'forward_signature', 'forward_sender_name', 'forward_date',
    'reply_to_message', 'via_bot', 'edit_date', 'media_group_id', 'author_signature',
    'text', 'entities', 'animation', 'audio', 'document', 'photo', 'sticker', 'video',
    'video_note', 'voice', 'caption', 'caption_entities', 'contact', 'dice', 'game',
    'poll', 'venue', 'location', 'new_chat_members', 'left_chat_member', 'new_chat_title',
    'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created',
    'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message',
    'connected_website', 'reply_markup']
    message_id              : int
    __from_u                : dict   = field(repr=False)
    from_u                  : 'User' = field(init=False)
    date                    : int 
    __chat                  : dict   = field(repr=False)
    chat                    : 'Chat' = field(init=False)
    __forward_from          : dict   = field(repr=False)
    forward_from            : 'User' = field(init=False)
    __forward_from_chat     : dict   = field(repr=False)
    forward_from_chat       : 'Chat' = field(init=False)
    forward_from_message_id : int
    forward_signature       : str
    forward_sender_name     : str
    forward_date            : int
    __reply_to_message      : dict   = field(repr=False)
    reply_to_message        : 'Message' = field(init=False)
    __via_bot               : dict   = field(repr=False)
    via_bot                 : 'User' = field(init=False)
    edit_date               : int
    media_group_id          : str
    author_signature        : str
    text                    : str
    entities                : list
    __animation             : dict   = field(repr=False)
    animation               : 'Animation' = field(init=False)
    __audio                 : dict    = field(repr=False)
    audio                   : 'Audio' = field(init=False)
    __document              : dict    = field(repr=False)
    document                : 'Document' = field(init=False)
    __photo                 : list    = field(repr=False)
    photo                   : List[PhotoSize] = field(init=False)
    __sticker               : dict   = field(repr=False)
    sticker                 : 'Sticker' = field(init=False)
    __video                 : dict   = field(repr=False)
    video                   : 'Video' = field(init=False)
    __video_note            : dict   = field(repr=False)
    video_note              : 'VideoNote' = field(init=False)
    __voice                 : dict   = field(repr=False)
    voice                   : 'Voice' = field(init=False)
    caption                 : str
    __caption_entities      : list   = field(repr=False)
    caption_entities        : List[MessageEntity] = field(init=False)
    __contact               : dict   = field(repr=False)
    contact                 : 'Contact' = field(init=False)
    __dice                  : dict   = field(repr=False)
    dice                    : 'Dice' = field(init=False)
    __game                  : dict   = field(repr=False)
    game                    : 'Game' = field(init=False)
    __poll                  : dict   = field(repr=False)
    poll                    : 'Poll' = field(init=False)
    __venue                 : dict   = field(repr=False)
    venue                   : 'Venue' = field(init=False)
    __location              : dict   = field(repr=False)
    location                : 'Location' = field(init=False)
    __new_chat_members      : list   = field(repr=False)
    new_chat_members        : List['User'] = field(init=False)
    __left_chat_member      : dict   = field(repr=False)
    left_chat_member        : 'User' = field(init=False)
    new_chat_title          : str 
    __newchat_photo         : list   = field(repr=False)
    new_chat_photo          : List[PhotoSize] = field(init=False)
    delete_chat_photo       : bool
    group_chat_created      : bool
    supergroup_chat_created : bool
    channel_chat_created    : bool
    migrate_to_chat_id      : int
    migrate_from_chat_id    : int
    __pinned_message        : dict   = field(repr=False)
    pinned_message          : 'Message' = field(init=False)
    connected_website       : str
    __reply_markup          : dict   = field(repr=False)
    reply_markup            : 'InlineKeyboardMarkup' = field(init=False)


    def __post_init__(self):
        self.from_u                  : 'User' = User.make_from_data(self.__from_u)
        self.chat                    : 'Chat' = Chat.make_from_data(self.__chat)
        self.forward_from            : 'User' = User.make_from_data(self.__forward_from)
        self.forward_from_chat       : 'Chat' = Chat.make_from_data(self.__forward_from_chat)
        self.reply_to_message        : 'Message' = Message.make_from_data(self.__reply_to_message)
        self.via_bot                 : 'User' = User.make_from_data(self.__via_bot)
        self.animation               : 'Animation' = Animation.make_from_data(self.__animation)
        self.audio                   : 'Audio' = Audio.make_from_data(self.__audio)
        self.document                : 'Document' = Document.make_from_data(self.__document)
        self.photo                   : List[PhotoSize] = PhotoSize.make_list_from_data(self.__photo)
        self.sticker                 : 'Sticker' = Sticker.make_from_data(self.__sticker)
        self.video                   : 'Video' = Video.make_from_data(self.__video)
        self.video_note              : 'VideoNote' = VideoNote.make_from_data(self.__video_note)
        self.voice                   : 'Voice' = Voice.make_from_data(self.__voice)
        self.caption_entities        : List[MessageEntity] = MessageEntity.make_list_from_data(self.__caption_entities)
        self.contact                 : 'Contact' = Contact.make_from_data(self.__contact)
        self.dice                    : 'Dice' = Dice.make_from_data(self.__dice)
        self.game                    : 'Game' = Game.make_from_data(self.__game)
        self.poll                    : 'Poll' = Poll.make_from_data(self.__poll)
        self.venue                   : 'Venue' = Venue.make_from_data(self.__venue)
        self.location                : 'Location' = Location.make_from_data(self.__location)
        self.new_chat_members        : List[User] = User.make_list_from_data(self.__new_chat_members)
        self.left_chat_member        : 'User' = User.make_from_data(self.__left_chat_member)
        self.new_chat_photo          : List[PhotoSize] = PhotoSize.make_list_from_data(self.__newchat_photo)
        self.pinned_message          : 'Message' = Message.make_from_data(self.__pinned_message)
        self.reply_markup            : 'InlineKeyboardMarkup' = InlineKeyboardMarkup.make_list_from_data(self.__reply_markup)

@dataclass
class CallbackQuery(FromIncomeData):
    KEYS = ['id', 'from', 'message', 'inline_message_id',
    'chat_instance', 'data', 'game_short_name']
    id               : str
    __from_u         : dict   = field(repr=False)
    from_u           : 'User' = field(init=False)
    __message        : dict   = field(repr=False)
    message          : 'Message' = field(init=False)
    inline_message_id: str
    chat_instance    : str
    data             : str
    game_short_name  : str

    def __post_init__(self):
        self.from_u : 'User' = User.make_from_data(self.__from_u)
        self.message: 'Message' = Message.make_from_data(self.__message)

@dataclass
class KeyboardButtonPollType(FromIncomeData):
    KEYS = ['type']
    type: str

@dataclass
class KeyboardButton(FromIncomeData):
    KEYS = ['text', 'request_contact', 'request_location', 'request_poll']
    text:str 
    request_contact: bool 
    request_location: bool
    __request_poll: dict = field(repr=False)
    request_poll: KeyboardButtonPollType = field(init=false)

    def __post_init__(self):
        self.request_poll = KeyboardButtonPollType.make_from_data(self.__request_poll)

@dataclass
class ReplyKeyboardMarkup(FromIncomeData):
    KEYS = ['keyboard','resize_keyboard','one_time_keyboard','selective']
    __keyboard       : list = field(repr=False)
    keyboard         : list = field(init=False)
    resize_keyboard  : bool
    one_time_keyboard: bool
    selective        : bool

    def __post_init__(self):
        self.keyboard = [InlineKeyboardButton.make_list_from_data(i) for i in self.__keyboard]

@dataclass
class ReplyKeyboardRemove(FromIncomeData):
    KEYS = ['remove_keyboard', 'selective']
    remove_keyboard: bool
    selective: bool

@dataclass
class ForceReply(FromIncomeData):
    KEYS = ['force_reply', 'selective']
    force_reply: bool 
    selective: bool