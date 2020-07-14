from typing import List
from dataclasses import dataclass, field

from datamix import FromIncomeData

class User(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        id           : int = raw.get('id')
        #Unique identifier for this user or bot
        is_bot       : bool = raw.get('is_bot')
        #True, if this user is a bot
        first_name   : str = raw.get('first_name')
        #User's or bot's first name
        last_name    : str = raw.get('last_name')
        #Optional. User's or bot's last name
        username     : str = raw.get('username')
        #Optional. User's or bot's username
        language_code: str = raw.get('language_code')
        #Optional. IETF language tag of the user's language
        can_join_groups            : bool = raw.get('can_join_groups', False)
        #Optional. True, if the bot can be invited to groups. Returned only in getMe.
        can_read_all_group_messages: bool = raw.get('can_read_all_group_messages', False)
        #Optional. True, if privacy mode is disabled for the bot. Returned only in getMe.
        supports_inline_queries    : bool = raw.get('supports_inline_queries', False)
        #Optional. True, if the bot supports inline queries. Returned only in getMe.
        return genObj

class ChatPhoto(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        small_file_id       : str = raw.get('small_file_id') 
        #File identifier of small (160x160) chat photo. This file_id can be used only for photo download and only for as long as the photo is not changed.
        small_file_unique_id: str = raw.get('small_file_unique_id') 
        #Unique file identifier of small (160x160) chat photo, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        big_file_id         : str = raw.get('big_file_id') 
        #File identifier of big (640x640) chat photo. This file_id can be used only for photo download and only for as long as the photo is not changed.
        big_file_unique_id  : str = raw.get('big_file_unique_id') 
        #Unique file identifier of big (640x640) chat photo, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        return genObj

class ChatPermissions(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        can_send_messages: bool = raw.get('can_send_messages', False)
        #Optional. True, if the user is allowed to send text messages, contacts, locations and venues
        can_send_media_messages: bool = raw.get('can_send_media_messages', False)
        #Optional. True, if the user is allowed to send audios, documents, photos, videos, video notes and voice notes, implies can_send_messages
        can_send_polls: bool = raw.get('can_send_polls', False)
        #Optional. True, if the user is allowed to send polls, implies can_send_messages
        can_send_other_messages: bool = raw.get('can_send_other_messages', False)
        #Optional. True, if the user is allowed to send animations, games, stickers and use inline bots, implies can_send_media_messages
        can_add_web_page_previews: bool = raw.get('can_add_web_page_previews', False)
        #Optional. True, if the user is allowed to add web page previews to their messages, implies can_send_media_messages
        can_change_info: bool = raw.get('can_change_info', False)
        #Optional. True, if the user is allowed to change the chat title, photo and other settings. Ignored in public supergroups
        can_invite_users: bool = raw.get('can_invite_users', False)
        #Optional. True, if the user is allowed to invite new users to the chat
        can_pin_messages: bool = raw.get('can_pin_messages', False)
        #Optional. True, if the user is allowed to pin messages. Ignored in public supergroups
        return genObj

class Chat(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        id: int = raw.get('id')
        #Unique identifier for this chat. This number may be greater than 32 bits and some programming languages may have difficulty/silent defects in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float type are safe for storing this identifier.
        type: str = raw.get('type')
        #Type of chat, can be either “private”, “group”, “supergroup” or “channel”
        title: str = raw.get('title')
        #Optional. Title, for supergroups, channels and group chats
        username: str = raw.get('username')
        #Optional. Username, for private chats, supergroups and channels if available
        first_name: str = raw.get('first_name')
        #Optional. First name of the other party in a private chat
        last_name: str = raw.get('last_name')
        #Optional. Last name of the other party in a private chat
        photo: 'ChatPhoto' = ChatPhoto.make_from_data(raw.get('photo', {}))
        #Optional. Chat photo. Returned only in getChat.
        description: str = raw.get('description')
        #Optional. Description, for groups, supergroups and channel chats. Returned only in getChat.
        invite_link: str = raw.get('invite_link')
        #Optional. Chat invite link, for groups, supergroups and channel chats. Each administrator in a chat generates their own invite links, so the bot must first generate the link using exportChatInviteLink. Returned only in getChat.
        pinned_message: 'Message' = raw.get('pinned_message', {})
        #Optional. Pinned message, for groups, supergroups and channels. Returned only in getChat.
        permissions: 'ChatPermissions' = ChatPermissions.make_from_data(raw.get('permissions', {}))
        #Optional. Default chat member permissions, for groups and supergroups. Returned only in getChat.
        slow_mode_delay: int = raw.get('slow_mode_delay')
        #Optional. For supergroups, the minimum allowed delay between consecutive messages sent by each unpriviledged user. Returned only in getChat.
        sticker_set_name: str = raw.get('sticker_set_name')
        #Optional. For supergroups, name of group sticker set. Returned only in getChat.
        can_set_sticker_set: bool = raw.get('can_set_sticker_set', False)
        #Optional. True, if the bot can change the group sticker set. Returned only in getChat.
        return genObj

class MessageEntity(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        type: str = raw.get('type')
        #Type of the entity. Can be “mention” (@username), “hashtag” (#hashtag), “cashtag” ($USD), “bot_command” (/start@jobs_bot), “url” (https://telegram.org), “email” (do-not-reply@telegram.org), “phone_number” (+1-212-555-0123), “bold” (bold text), “italic” (italic text), “underline” (underlined text), “strikethrough” (strikethrough text), “code” (monowidth string), “pre” (monowidth block), “text_link” (for clickable text URLs), “text_mention” (for users without usernames)
        offset: int = raw.get('offset')
        #Offset in UTF-16 code units to the start of the entity
        length: int = raw.get('length')
        #Length of the entity in UTF-16 code units
        url: str = raw.get('url')
        #Optional. For “text_link” only, url that will be opened after user taps on the text
        user: 'User' = User.make_from_data(raw.get('user', {}))
        #Optional. For “text_mention” only, the mentioned user
        language: str = raw.get('language')
        #Optional. For “pre” only, the programming language of the entity text
        return genObj

class PhotoSize(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        file_id: str = raw.get('file_id')
        #Identifier for this file, which can be used to download or reuse the file
        file_unique_id: str = raw.get('file_unique_id')
        #Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        width: int = raw.get('width')
        #Photo width
        height: int = raw.get('height')
        #Photo height
        file_size: int = raw.get('file_size')
        #Optional. File size
        return genObj

#TODO data reused class

class Animation(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        file_id: str = raw.get('file_id')
        #Identifier for this file, which can be used to download or reuse the file
        file_unique_id: str = raw.get('file_unique_id')
        #Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        width: int = raw.get('width')
        #Video width as defined by sender
        height: int = raw.get('height')
        #Video height as defined by sender
        duration: int = raw.get('duration')
        #Duration of the video in seconds as defined by sender
        thumb: 'PhotoSize' = PhotoSize.make_from_data(raw.get('thumb', {}))
        #Optional. Animation thumbnail as defined by sender
        file_name: str = raw.get('file_name')
        #Optional. Original animation filename as defined by sender
        mime_type: str = raw.get('mime_type')
        #Optional. MIME type of the file as defined by sender
        file_size: int = raw.get('file_size')
        #Optional. File size
        return genObj

class Audio(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        file_id: str = raw.get('file_id')
        #Identifier for this file, which can be used to download or reuse the file
        file_unique_id: str = raw.get('file_unique_id')
        #Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        duration: int = raw.get('duration')
        #Duration of the audio in seconds as defined by sender
        performer: str = raw.get('performer')
        #Optional. Performer of the audio as defined by sender or by audio tags
        title: str = raw.get('title')
        #Optional. Title of the audio as defined by sender or by audio tags
        mime_type: str = raw.get('mime_type')
        #Optional. MIME type of the file as defined by sender
        file_size: int = raw.get('file_size')
        #Optional. File size
        thumb: 'PhotoSize' = PhotoSize.make_from_data(raw.get('thumb', {}))
        #Optional. Thumbnail of the album cover to which the music file belongs
        return genObj

class Document(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        file_id: str = raw.get('file_id')
        #Identifier for this file, which can be used to download or reuse the file
        file_unique_id: str = raw.get('file_unique_id')
        #Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        thumb: 'PhotoSize' = PhotoSize.make_from_data(raw.get('thumb', {}))
        #Optional. Document thumbnail as defined by sender
        file_name: str = raw.get('file_name')
        #Optional. Original filename as defined by sender
        mime_type: str = raw.get('mime_type')
        #Optional. MIME type of the file as defined by sender
        file_size: int = raw.get('file_size') #Optional. File size
        return genObj

class MaskPosition(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        point: str = raw.get('point')
        #The part of the face relative to which the mask should be placed. One of “forehead”, “eyes”, “mouth”, or “chin”.
        x_shift: float = raw.get('x_shift')
        #Shift by X-axis measured in widths of the mask scaled to the face size, from left to right. For example, choosing -1.0 will place mask just to the left of the default mask position.
        y_shift: float = raw.get('y_shift')
        #Shift by Y-axis measured in heights of the mask scaled to the face size, from top to bottom. For example, 1.0 will place the mask just below the default mask position.
        scale: float = raw.get('scale')
        #Mask scaling coefficient. For example, 2.0 means double size.
        return genObj

class Sticker(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        file_id: str = raw.get('file_id')
        #Identifier for this file, which can be used to download or reuse the file
        file_unique_id: str = raw.get('file_unique_id')
        #Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        width: int = raw.get('width')
        #Sticker width
        height: int = raw.get('height')
        #Sticker height
        is_animated: bool = raw.get('is_animated', False)
        #True, if the sticker is animated
        thumb: 'PhotoSize' = PhotoSize.make_from_data(raw.get('thumb', {}))
        #Optional. Sticker thumbnail in the .WEBP or .JPG format
        emoji: str = raw.get('emoji')
        #Optional. Emoji associated with the sticker
        set_name: str = raw.get('set_name')
        #Optional. Name of the sticker set to which the sticker belongs
        mask_position: 'MaskPosition' = MaskPosition.make_from_data(raw.get('mask_position', {}))
        #Optional. For mask stickers, the position where the mask should be placed
        file_size: int = raw.get('file_size')
        #Optional. File size
        return genObj

class Video(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        file_id: str = raw.get('file_id')
        #Identifier for this file, which can be used to download or reuse the file
        file_unique_id: str = raw.get('file_unique_id')
        #Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        width: int = raw.get('width')
        #Video width as defined by sender
        height: int = raw.get('height')
        #Video height as defined by sender
        duration: int = raw.get('duration')
        #Duration of the video in seconds as defined by sender
        thumb: 'PhotoSize' = PhotoSize.make_from_data(raw.get('thumb', {}))
        #Optional. Video thumbnail
        mime_type: str = raw.get('mime_type')
        #Optional. Mime type of a file as defined by sender
        file_size: int = raw.get('file_size')
        #Optional. File size
        return genObj

class VideoNote(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        file_id: str = raw.get('file_id')
        #Identifier for this file, which can be used to download or reuse the file
        file_unique_id: str = raw.get('file_unique_id')
        #Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        length: int = raw.get('length')
        #Video width and height (diameter of the video message) as defined by sender
        duration: int = raw.get('duration')
        #Duration of the video in seconds as defined by sender
        thumb: 'PhotoSize' = PhotoSize.make_from_data(raw.get('thumb', {}))
        #Optional. Video thumbnail
        file_size: int = raw.get('file_size')
        #Optional. File size
        return genObj

class Voice(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        file_id: str = raw.get('file_id')
        #Identifier for this file, which can be used to download or reuse the file
        file_unique_id: str = raw.get('file_unique_id')
        #Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        duration: int = raw.get('duration')
        #Duration of the audio in seconds as defined by sender
        mime_type: str = raw.get('mime_type')
        #Optional. MIME type of the file as defined by sender
        file_size: int = raw.get('file_size')
        #Optional. File size
        return genObj

class Contact(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        phone_number: str = raw.get('phone_number')
        #Contact's phone number
        first_name: str = raw.get('first_name')
        #Contact's first name
        last_name: str = raw.get('last_name')
        #Optional. Contact's last name
        user_id: int = raw.get('user_id')
        #Optional. Contact's user identifier in Telegram
        vcard: str = raw.get('vcard')
        #Optional. Additional data about the contact in the form of a vCard
        return genObj

class Dice(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        emoji: str = raw.get('emoji')
        #Emoji on which the dice throw animation is based
        value: int = raw.get('value')
        #Value of the dice, 1-6 for “🎲” and “🎯” base emoji, 1-5 for “🏀” base emoji
        return genObj

class Game(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        title: str = raw.get('title')
        #Title of the game
        description: str = raw.get('description')
        #Description of the game
        photo: list = [PhotoSize.make_from_data(i) for i in raw.get('photo')]
        #Photo that will be displayed in the game message in chats.
        text: str = raw.get('text')
        #Optional. Brief description of the game or high scores included in the game message. Can be automatically edited to include current high scores for the game when the bot calls setGameScore, or manually edited using editMessageText. 0-4096 characters.
        text_entities: list = [MessageEntity.make_from_data(i) for i in raw.get('text_entities', [])]
        #Optional. Special entities that appear in text, such as usernames, URLs, bot commands, etc.
        animation: 'Animation' = Animation.make_from_data(raw.get('animation', {}))
        #Optional. Animation that will be displayed in the game message in chats. Upload via BotFather
        return genObj

class PollOption(FromIncomeData):
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        text: str = raw.get('text')
        #Option text, 1-100 characters
        voter_count: int = raw.get('voter_count')
        #Number of users that voted for this option
        return genObj

class Poll(FromIncomeData):
    id: str = raw.get('id')
    #Unique poll identifier
    question: str = raw.get('question')
    #Poll question, 1-255 characters
    options: list = [PollOption(i) for i in raw.get('options')]
    #List of poll options
    total_voter_count: int = raw.get('total_voter_count')
    #Total number of users that voted in the poll
    is_closed: bool = raw.get('is_closed')
    #  True, if the poll is closed
    is_anonymous: bool = raw.get('is_anonymous')
    #   True, if the poll is anonymous
    type: str = raw.get('type')
    #Poll type, currently can be “regular” or “quiz”
    allows_multiple_answers: bool = raw.get('allows_multiple_answers')
    #True, if the poll allows multiple answers
    correct_option_id: int = raw.get('correct_option_id')
    #Optional. 0-based identifier of the correct answer option. Available only for polls in the quiz mode, which are closed, or was sent (not forwarded) by the bot or to the private chat with the bot.
    explanation: str = raw.get('explanation')
    #Optional. Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll, 0-200 characters
    explanation_entities: list = [MessageEntity(i) for i in raw.get('explanation_entities', [])]
    #Optional. Special entities like usernames, URLs, bot commands, etc. that appear in the explanation
    open_period: int = raw.get('open_period')
    #Optional. Amount of time in seconds the poll will be active after creation
    close_date: int = raw.get('close_date')
    #Optional. Point in time (Unix timestamp) when the poll will be automatically closed
    return genObj

class Location(FromIncomeData):
    KEYS = ['longitude', 'latitude']
    longitude: float
    latitude: float

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

class SuccessfulPayment(FromIncomeData):
    pass

class PassportData(FromIncomeData):
    pass

class LoginUrl(FromIncomeData):
    KEYS = ['url', 'forward_text', 'bot_username', 'request_write_access']
    url: str
    forward_text: str
    bot_username: str
    request_write_access: bool

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
        from_u                  : 'User' = User.make_from_data(self.__from_u)
        chat                    : 'Chat' = Chat.make_from_data(self.__chat)
        forward_from            : 'User' = User.make_from_data(self.__forward_from)
        forward_from_chat       : 'Chat' = Chat.make_from_data(self.__forward_from_chat)
        reply_to_message        : 'Message' = Message.make_from_data(self.__reply_to_message)
        via_bot                 : 'User' = User.make_from_data(self.__via_bot)
        animation               : 'Animation' = Animation.make_from_data(self.__animation)
        audio                   : 'Audio' = Audio.make_from_data(self.__audio)
        document                : 'Document' = Document.make_from_data(self.__document)
        photo                   : List[PhotoSize] = PhotoSize.make_list_from_data(self.__photo)
        sticker                 : 'Sticker' = Sticker.make_from_data(self.__sticker)
        video                   : 'Video' = Video.make_from_data(self.__video)
        video_note              : 'VideoNote' = VideoNote.make_from_data(self.__video_note)
        voice                   : 'Voice' = Voice.make_from_data(self.__voice)
        caption_entities        : List[MessageEntity] = MessageEntity.make_list_from_data(self.__caption_entities)
        contact                 : 'Contact' = Contact.make_from_data(self.__contact)
        dice                    : 'Dice' = Dice.make_from_data(self.__dice)
        game                    : 'Game' = Game.make_from_data(self.__game)
        poll                    : 'Poll' = Poll.make_from_data(self.__poll)
        venue                   : 'Venue' = Venue.make_from_data(self.__venue)
        location                : 'Location' = Location.make_from_data(self.__location)
        new_chat_members        : List['User'] = User.make_list_from_data(self.__new_chat_members)
        left_chat_member        : 'User' = User.make_from_data(self.__left_chat_member)
        new_chat_photo          : List[PhotoSize] = PhotoSize.make_list_from_data(self.__new_chat_photo)
        pinned_message          : 'Message' Message.make_from_data(self.__pinned_message)
        reply_markup            : 'InlineKeyboardMarkup' = InlineKeyboardMarkup.make_list_from_data(self.__reply_markup)

@dataclass
class CallbackQuery:
    @classmethod
    def make_from_data(cls, raw):
        if not raw:
            return None
        genObj = cls()
        id: str = raw.get('id')
        #Unique identifier for this query
        from_u: 'User' = raw.get('from')
        #Sender
        message: 'Message' = raw.get('message')
        #Optional. Message with the callback button that originated the query. Note that message content and message date will not be available if the message is too old
        inline_message_id: str = raw.get('inline_message_id')
        #Optional. Identifier of the message sent via the bot in inline mode, that originated the query.
        chat_instance: str = raw.get('chat_instance')
        #Global identifier, uniquely corresponding to the chat to which the message with the callback button was sent. Useful for high scores in games.
        data: str = raw.get('data')
        #Optional. Data associated with the callback button. Be aware that a bad client can send arbitrary data in this field.
        game_short_name: str = raw.get('game_short_name')
        #Optional. Short name of a Game to be returned, serves as the unique identifier for the game
        if _check_self():
            return genObj
        return None