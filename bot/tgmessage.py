class User:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.id           : int = raw.get('id')
        #Unique identifier for this user or bot
        cls.is_bot       : bool = raw.get('is_bot')
        #True, if this user is a bot
        cls.first_name   : str = raw.get('first_name')
        #User's or bot's first name
        cls.last_name    : str = raw.get('last_name')
        #Optional. User's or bot's last name
        cls.username     : str = raw.get('username')
        #Optional. User's or bot's username
        cls.language_code: str = raw.get('language_code')
        #Optional. IETF language tag of the user's language
        cls.can_join_groups            : bool = raw.get('can_join_groups', False)
        #Optional. True, if the bot can be invited to groups. Returned only in getMe.
        cls.can_read_all_group_messages: bool = raw.get('can_read_all_group_messages', False)
        #Optional. True, if privacy mode is disabled for the bot. Returned only in getMe.
        cls.supports_inline_queries    : bool = raw.get('supports_inline_queries', False)
        #Optional. True, if the bot supports inline queries. Returned only in getMe.
        return cls()

class ChatPhoto:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.small_file_id       : str = raw.get('small_file_id') 
        #File identifier of small (160x160) chat photo. This file_id can be used only for photo download and only for as long as the photo is not changed.
        cls.small_file_unique_id: str = raw.get('small_file_unique_id') 
        #Unique file identifier of small (160x160) chat photo, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        cls.big_file_id         : str = raw.get('big_file_id') 
        #File identifier of big (640x640) chat photo. This file_id can be used only for photo download and only for as long as the photo is not changed.
        cls.big_file_unique_id  : str = raw.get('big_file_unique_id') 
        #Unique file identifier of big (640x640) chat photo, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        return cls()

class ChatPermissions:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.can_send_messages: bool = raw.get('can_send_messages', False)
        #Optional. True, if the user is allowed to send text messages, contacts, locations and venues
        cls.can_send_media_messages: bool = raw.get('can_send_media_messages', False)
        #Optional. True, if the user is allowed to send audios, documents, photos, videos, video notes and voice notes, implies can_send_messages
        cls.can_send_polls: bool = raw.get('can_send_polls', False)
        #Optional. True, if the user is allowed to send polls, implies can_send_messages
        cls.can_send_other_messages: bool = raw.get('can_send_other_messages', False)
        #Optional. True, if the user is allowed to send animations, games, stickers and use inline bots, implies can_send_media_messages
        cls.can_add_web_page_previews: bool = raw.get('can_add_web_page_previews', False)
        #Optional. True, if the user is allowed to add web page previews to their messages, implies can_send_media_messages
        cls.can_change_info: bool = raw.get('can_change_info', False)
        #Optional. True, if the user is allowed to change the chat title, photo and other settings. Ignored in public supergroups
        cls.can_invite_users: bool = raw.get('can_invite_users', False)
        #Optional. True, if the user is allowed to invite new users to the chat
        cls.can_pin_messages: bool = raw.get('can_pin_messages', False)
        #Optional. True, if the user is allowed to pin messages. Ignored in public supergroups
        return cls()

class Chat:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.id: int = raw.get('id')
        #Unique identifier for this chat. This number may be greater than 32 bits and some programming languages may have difficulty/silent defects in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float type are safe for storing this identifier.
        cls.type: str = raw.get('type')
        #Type of chat, can be either “private”, “group”, “supergroup” or “channel”
        cls.title: str = raw.get('title')
        #Optional. Title, for supergroups, channels and group chats
        cls.username: str = raw.get('username')
        #Optional. Username, for private chats, supergroups and channels if available
        cls.first_name: str = raw.get('first_name')
        #Optional. First name of the other party in a private chat
        cls.last_name: str = raw.get('last_name')
        #Optional. Last name of the other party in a private chat
        cls.photo: 'ChatPhoto' = ChatPhoto.gen(raw.get('photo', {}))
        #Optional. Chat photo. Returned only in getChat.
        cls.description: str = raw.get('description')
        #Optional. Description, for groups, supergroups and channel chats. Returned only in getChat.
        cls.invite_link: str = raw.get('invite_link')
        #Optional. Chat invite link, for groups, supergroups and channel chats. Each administrator in a chat generates their own invite links, so the bot must first generate the link using exportChatInviteLink. Returned only in getChat.
        cls.pinned_message: 'Message' = raw.get('pinned_message', {})
        #Optional. Pinned message, for groups, supergroups and channels. Returned only in getChat.
        cls.permissions: 'ChatPermissions' = ChatPermissions.gen(raw.get('permissions', {}))
        #Optional. Default chat member permissions, for groups and supergroups. Returned only in getChat.
        cls.slow_mode_delay: int = raw.get('slow_mode_delay')
        #Optional. For supergroups, the minimum allowed delay between consecutive messages sent by each unpriviledged user. Returned only in getChat.
        cls.sticker_set_name: str = raw.get('sticker_set_name')
        #Optional. For supergroups, name of group sticker set. Returned only in getChat.
        cls.can_set_sticker_set: bool = raw.get('can_set_sticker_set', False)
        #Optional. True, if the bot can change the group sticker set. Returned only in getChat.
        return cls()

class MessageEntity:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.type: str = raw.get('type')
        #Type of the entity. Can be “mention” (@username), “hashtag” (#hashtag), “cashtag” ($USD), “bot_command” (/start@jobs_bot), “url” (https://telegram.org), “email” (do-not-reply@telegram.org), “phone_number” (+1-212-555-0123), “bold” (bold text), “italic” (italic text), “underline” (underlined text), “strikethrough” (strikethrough text), “code” (monowidth string), “pre” (monowidth block), “text_link” (for clickable text URLs), “text_mention” (for users without usernames)
        cls.offset: int = raw.get('offset')
        #Offset in UTF-16 code units to the start of the entity
        cls.length: int = raw.get('length')
        #Length of the entity in UTF-16 code units
        cls.url: str = raw.get('url')
        #Optional. For “text_link” only, url that will be opened after user taps on the text
        cls.user: 'User' = User.gen(raw.get('user', {}))
        #Optional. For “text_mention” only, the mentioned user
        cls.language: str = raw.get('language')
        #Optional. For “pre” only, the programming language of the entity text
        return cls()

class PhotoSize:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.file_id: str = raw.get('file_id')
        #Identifier for this file, which can be used to download or reuse the file
        cls.file_unique_id: str = raw.get('file_unique_id')
        #Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        cls.width: int = raw.get('width')
        #Photo width
        cls.height: int = raw.get('height')
        #Photo height
        cls.file_size: int = raw.get('file_size')
        #Optional. File size
        return cls()

#TODO data reused class

class Animation:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.file_id: str = raw.get('file_id')
        #Identifier for this file, which can be used to download or reuse the file
        cls.file_unique_id: str = raw.get('file_unique_id')
        #Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        cls.width: int = raw.get('width')
        #Video width as defined by sender
        cls.height: int = raw.get('height')
        #Video height as defined by sender
        cls.duration: int = raw.get('duration')
        #Duration of the video in seconds as defined by sender
        cls.thumb: 'PhotoSize' = PhotoSize.gen(raw.get('thumb', {}))
        #Optional. Animation thumbnail as defined by sender
        cls.file_name: str = raw.get('file_name')
        #Optional. Original animation filename as defined by sender
        cls.mime_type: str = raw.get('mime_type')
        #Optional. MIME type of the file as defined by sender
        cls.file_size: int = raw.get('file_size')
        #Optional. File size
        return cls()

class Audio:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.file_id: str = raw.get('file_id')
        #Identifier for this file, which can be used to download or reuse the file
        cls.file_unique_id: str = raw.get('file_unique_id')
        #Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        cls.duration: int = raw.get('duration')
        #Duration of the audio in seconds as defined by sender
        cls.performer: str = raw.get('performer')
        #Optional. Performer of the audio as defined by sender or by audio tags
        cls.title: str = raw.get('title')
        #Optional. Title of the audio as defined by sender or by audio tags
        cls.mime_type: str = raw.get('mime_type')
        #Optional. MIME type of the file as defined by sender
        cls.file_size: int = raw.get('file_size')
        #Optional. File size
        cls.thumb: 'PhotoSize' = PhotoSize.gen(raw.get('thumb', {}))
        #Optional. Thumbnail of the album cover to which the music file belongs
        return cls()

class Document:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.file_id: str = raw.get('file_id')
        #Identifier for this file, which can be used to download or reuse the file
        cls.file_unique_id: str = raw.get('file_unique_id')
        #Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        cls.thumb: 'PhotoSize' = PhotoSize.gen(raw.get('thumb', {}))
        #Optional. Document thumbnail as defined by sender
        cls.file_name: str = raw.get('file_name')
        #Optional. Original filename as defined by sender
        cls.mime_type: str = raw.get('mime_type')
        #Optional. MIME type of the file as defined by sender
        cls.file_size: int = raw.get('file_size') #Optional. File size
        return cls()

class MaskPosition:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.point: str = raw.get('point')
        #The part of the face relative to which the mask should be placed. One of “forehead”, “eyes”, “mouth”, or “chin”.
        cls.x_shift: float = raw.get('x_shift')
        #Shift by X-axis measured in widths of the mask scaled to the face size, from left to right. For example, choosing -1.0 will place mask just to the left of the default mask position.
        cls.y_shift: float = raw.get('y_shift')
        #Shift by Y-axis measured in heights of the mask scaled to the face size, from top to bottom. For example, 1.0 will place the mask just below the default mask position.
        cls.scale: float = raw.get('scale')
        #Mask scaling coefficient. For example, 2.0 means double size.
        return cls()

class Sticker:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.file_id: str = raw.get('file_id')
        #Identifier for this file, which can be used to download or reuse the file
        cls.file_unique_id: str = raw.get('file_unique_id')
        #Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        cls.width: int = raw.get('width')
        #Sticker width
        cls.height: int = raw.get('height')
        #Sticker height
        cls.is_animated: bool = raw.get('is_animated', False)
        #True, if the sticker is animated
        cls.thumb: 'PhotoSize' = PhotoSize.gen(raw.get('thumb', {}))
        #Optional. Sticker thumbnail in the .WEBP or .JPG format
        cls.emoji: str = raw.get('emoji')
        #Optional. Emoji associated with the sticker
        cls.set_name: str = raw.get('set_name')
        #Optional. Name of the sticker set to which the sticker belongs
        cls.mask_position: 'MaskPosition' = MaskPosition.gen(raw.get('mask_position', {}))
        #Optional. For mask stickers, the position where the mask should be placed
        cls.file_size: int = raw.get('file_size')
        #Optional. File size
        return cls()

class Video:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.file_id: str = raw.get('file_id')
        #Identifier for this file, which can be used to download or reuse the file
        cls.file_unique_id: str = raw.get('file_unique_id')
        #Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        cls.width: int = raw.get('width')
        #Video width as defined by sender
        cls.height: int = raw.get('height')
        #Video height as defined by sender
        cls.duration: int = raw.get('duration')
        #Duration of the video in seconds as defined by sender
        cls.thumb: 'PhotoSize' = PhotoSize.gen(raw.get('thumb', {}))
        #Optional. Video thumbnail
        cls.mime_type: str = raw.get('mime_type')
        #Optional. Mime type of a file as defined by sender
        cls.file_size: int = raw.get('file_size')
        #Optional. File size
        return cls()

class VideoNote:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.file_id: str = raw.get('file_id')
        #Identifier for this file, which can be used to download or reuse the file
        cls.file_unique_id: str = raw.get('file_unique_id')
        #Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        cls.length: int = raw.get('length')
        #Video width and height (diameter of the video message) as defined by sender
        cls.duration: int = raw.get('duration')
        #Duration of the video in seconds as defined by sender
        cls.thumb: 'PhotoSize' = PhotoSize.gen(raw.get('thumb', {}))
        #Optional. Video thumbnail
        cls.file_size: int = raw.get('file_size')
        #Optional. File size
        return cls()

class Voice:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.file_id: str = raw.get('file_id')
        #Identifier for this file, which can be used to download or reuse the file
        cls.file_unique_id: str = raw.get('file_unique_id')
        #Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        cls.duration: int = raw.get('duration')
        #Duration of the audio in seconds as defined by sender
        cls.mime_type: str = raw.get('mime_type')
        #Optional. MIME type of the file as defined by sender
        cls.file_size: int = raw.get('file_size')
        #Optional. File size
        return cls()

class Contact:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.phone_number: str = raw.get('phone_number')
        #Contact's phone number
        cls.first_name: str = raw.get('first_name')
        #Contact's first name
        cls.last_name: str = raw.get('last_name')
        #Optional. Contact's last name
        cls.user_id: int = raw.get('user_id')
        #Optional. Contact's user identifier in Telegram
        cls.vcard: str = raw.get('vcard')
        #Optional. Additional data about the contact in the form of a vCard
        return cls()

class Dice:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.emoji: str = raw.get('emoji')
        #Emoji on which the dice throw animation is based
        cls.value: int = raw.get('value')
        #Value of the dice, 1-6 for “🎲” and “🎯” base emoji, 1-5 for “🏀” base emoji
        return cls()

class Game:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.title: str = raw.get('title')
        #Title of the game
        cls.description: str = raw.get('description')
        #Description of the game
        cls.photo: list = [PhotoSize.gen(i) for i in raw.get('photo')]
        #Photo that will be displayed in the game message in chats.
        cls.text: str = raw.get('text')
        #Optional. Brief description of the game or high scores included in the game message. Can be automatically edited to include current high scores for the game when the bot calls setGameScore, or manually edited using editMessageText. 0-4096 characters.
        cls.text_entities: list = [MessageEntity.gen(i) for i in raw.get('text_entities', [])]
        #Optional. Special entities that appear in text, such as usernames, URLs, bot commands, etc.
        cls.animation: 'Animation' = Animation.gen(raw.get('animation', {}))
        #Optional. Animation that will be displayed in the game message in chats. Upload via BotFather
        return cls()

class PollOption:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.text: str = raw.get('text')
        #Option text, 1-100 characters
        cls.voter_count: int = raw.get('voter_count')
        #Number of users that voted for this option
        return cls()

class Poll:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.id: str = raw.get('id')
        #Unique poll identifier
        cls.question: str = raw.get('question')
        #Poll question, 1-255 characters
        cls.options: list = [PollOption(i) for i in raw.get('options')]
        #List of poll options
        cls.total_voter_count: int = raw.get('total_voter_count')
        #Total number of users that voted in the poll
        cls.is_closed: bool = raw.get('is_closed')
        #  True, if the poll is closed
        cls.is_anonymous: bool = raw.get('is_anonymous')
        #   True, if the poll is anonymous
        cls.type: str = raw.get('type')
        #Poll type, currently can be “regular” or “quiz”
        cls.allows_multiple_answers: bool = raw.get('allows_multiple_answers')
        #True, if the poll allows multiple answers
        cls.correct_option_id: int = raw.get('correct_option_id')
        #Optional. 0-based identifier of the correct answer option. Available only for polls in the quiz mode, which are closed, or was sent (not forwarded) by the bot or to the private chat with the bot.
        cls.explanation: str = raw.get('explanation')
        #Optional. Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll, 0-200 characters
        cls.explanation_entities: list = [MessageEntity(i) for i in raw.get('explanation_entities', [])]
        #Optional. Special entities like usernames, URLs, bot commands, etc. that appear in the explanation
        cls.open_period: int = raw.get('open_period')
        #Optional. Amount of time in seconds the poll will be active after creation
        cls.close_date: int = raw.get('close_date')
        #Optional. Point in time (Unix timestamp) when the poll will be automatically closed
        return cls()

class Location:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.longitude: float = raw.get('longitude')
        #Longitude as defined by sender
        cls.latitude: float = raw.get('latitude')
        #Latitude as defined by sender
        return cls()

class Venue:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.location: 'Location' = Location.gen(raw.get('location'))
        #Venue location
        cls.title: str = raw.get('title')
        #Name of the venue
        cls.address: str = raw.get('address')
        #Address of the venue
        cls.foursquare_id: str = raw.get('foursquare_id')
        #Optional. Foursquare identifier of the venue
        cls.foursquare_type: str = raw.get('foursquare_type')
        #Optional. Foursquare type of the venue. (For example, “arts_entertainment/default”, “arts_entertainment/aquarium” or “food/icecream”.)
        return cls()

class SuccessfulPayment:
    pass

class PassportData:
    pass

class LoginUrl:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.url: str = raw.get('url')
        #An HTTP URL to be opened with user authorization data added to the query string when the button is pressed. If the user refuses to provide authorization data, the original URL without information about the user will be opened. The data added is the same as described in Receiving authorization data.
        #NOTE: You must always check the hash of the received data to verify the authentication and the integrity of the data as described in Checking authorization.
        cls.forward_text: str = raw.get('forward_text')
        #Optional. New text of the button in forwarded messages.
        cls.bot_username: str = raw.get('bot_username')
        #Optional. Username of a bot, which will be used for user authorization. See Setting up a bot for more details. If not specified, the current bot's username will be assumed. The url's domain must be the same as the domain linked with the bot. See Linking your domain to the bot for more details.
        cls.request_write_access: bool = raw.get('request_write_access')
        #Optional. Pass True to request the permission for your bot to send messages to the user.
        return cls()

class InlineKeyboardButton:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.text: str = raw.get('')
        #Label text on the button
        cls.url: str = raw.get('')
        #Optional. HTTP or tg:// url to be opened when button is pressed
        cls.login_url: 'LoginUrl' = LoginUrl.gen(raw.get('login_url', {}))
        #Optional. An HTTP URL used to automatically authorize the user. Can be used as a replacement for the Telegram Login Widget.
        cls.callback_data: str = raw.get('callback_data')
        #Optional. Data to be sent in a callback query to the bot when button is pressed, 1-64 bytes
        cls.switch_inline_query: str = raw.get('switch_inline_query')
        #Optional. If set, pressing the button will prompt the user to select one of their chats, open that chat and insert the bot's username and the specified inline query in the input field. Can be empty, in which case just the bot's username will be inserted.
        #Note: This offers an easy way for users to start using your bot in inline mode when they are currently in a private chat with it. Especially useful when combined with switch_pm… actions – in this case the user will be automatically returned to the chat they switched from, skipping the chat selection screen.
        cls.switch_inline_query_current_chat: str = raw.get('switch_inline_query_current_chat')
        #Optional. If set, pressing the button will insert the bot's username and the specified inline query in the current chat's input field. Can be empty, in which case only the bot's username will be inserted.
        #This offers a quick way for the user to open your bot in inline mode in the same chat – good for selecting something from multiple options.
        #TODO callback_game	CallbackGame	Optional. Description of the game that will be launched when the user presses the button.
        #NOTE: This type of button must always be the first button in the first row.
        cls.pay: bool = raw.get('pay')
        #Optional. Specify True, to send a Pay button.
        #NOTE: This type of button must always be the first button in the first row.
        return cls()

class InlineKeyboardMarkup:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.inline_keyboard: list = [[InlineKeyboardButton.gen(j) for j in i] for i in raw.get('inline_keyboard', [])]
        #Array of button rows, each represented by an Array of InlineKeyboardButton objects
        return cls()

class Message:
    message_id: int
    date: int 
    chat: 'Chat'
    
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.message_id: int = raw.get('message_id')
        #Unique message identifier inside this chat
        cls.from_u: 'User' = User.gen(raw.get('user', {}))
        #Optional. Sender, empty for messages sent to channels
        cls.date: int = raw.get('date')
        #Date the message was sent in Unix time
        cls.chat: 'Chat' = Chat.gen(raw.get('chat', {}))
        #Conversation the message belongs to
        cls.forward_from: 'User' = User.gen(raw.get('forward_from', {}))
        #Optional. For forwarded messages, sender of the original message
        cls.forward_from_chat: 'Chat' = Chat.gen(raw.get('forward_from_chat', {}))
        #Optional. For messages forwarded from channels, information about the original channel
        cls.forward_from_message_id: int = raw.get('forward_from_message_id')
        #Optional. For messages forwarded from channels, identifier of the original message in the channel
        cls.forward_signature: str = raw.get('forward_signature')
        #Optional. For messages forwarded from channels, signature of the post author if present
        cls.forward_sender_name: str = raw.get('forward_sender_name')
        #Optional. Sender's name for messages forwarded from users who disallow adding a link to their account in forwarded messages
        cls.forward_date: int = raw.get('forward_date') #
        #Optional. For forwarded messages, date the original message was sent in Unix time
        cls.reply_to_message: 'Message' = Message.gen(raw.get('reply_to_message'))
        #Optional. For replies, the original message. Note that the Message object in this field will not contain further reply_to_message fields even if it itcls is a reply.
        cls.via_bot: 'User' =  User.gen(raw.get('via_bot', {}))
        #Optional. Bot through which the message was sent
        cls.edit_date: int = raw.get('edit_date')
        #Optional. Date the message was last edited in Unix time
        cls.media_group_id: str = raw.get('media_group_id')
        #Optional. The unique identifier of a media message group this message belongs to
        cls.author_signature: str = raw.get('author_signature')
        #Optional. Signature of the post author for messages in channels
        cls.text: str = raw.get('text')
        #Optional. For text messages, the actual UTF-8 text of the message, 0-4096 characters
        cls.entities: list = [MessageEntity.gen(i) for i in raw.get('entities', [])]
        #Optional. For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text
        cls.animation: 'Animation' = Animation.gen(raw.get('animation'))
        #Optional. Message is an animation, information about the animation. For backward compatibility, when this field is set, the document field will also be set
        cls.audio: 'Audio' = Audio.gen(raw.get('audio'))
        #Optional. Message is an audio file, information about the file
        cls.document: 'Document' = Document.gen(raw.get('document'))
        #Optional. Message is a general file, information about the file
        cls.photo: list = [PhotoSize.gen(i) for i in raw.get('photo', {})]
        #Optional. Message is a photo, available sizes of the photo
        cls.sticker: 'Sticker' = Sticker.gen(raw.get('sticker'))
        #Optional. Message is a sticker, information about the sticker
        cls.video: 'Video' = Video.gen(raw.get('video'))
        #Optional. Message is a video, information about the video
        cls.video_note: 'VideoNote' = VideoNote.gen(raw.get('video_note'))
        #Optional. Message is a video note, information about the video message
        cls.voice: 'Voice' = Voice.gen(raw.get('voice'))
        #Optional. Message is a voice message, information about the file
        cls.caption: str = raw.get('caption')
        #Optional. Caption for the animation, audio, document, photo, video or voice, 0-1024 characters
        cls.caption_entities: list = [MessageEntity.gen(i) for i in raw.get('caption_entities', [])]
        #Optional. For messages with a caption, special entities like usernames, URLs, bot commands, etc. that appear in the caption
        cls.contact: 'Contact' = Contact.gen(raw.get('contact'))
        #Optional. Message is a shared contact, information about the contact
        cls.dice: 'Dice' = Dice.gen(raw.get('dice'))
        #Optional. Message is a dice with random value from 1 to 6
        cls.game: 'Game' = Game.gen(raw.get('game'))
        #Optional. Message is a game, information about the game. More about games »
        cls.poll: 'Poll' = Poll.gen(raw.get('poll'))
        #Optional. Message is a native poll, information about the poll
        cls.venue: 'Venue' = Venue.gen(raw.get('venue'))
        #Optional. Message is a venue, information about the venue. For backward compatibility, when this field is set, the location field will also be set
        cls.location: 'Location' = Location.gen(raw.get('location'))
        #Optional. Message is a shared location, information about the location
        cls.new_chat_members: list = [User.gen(i) for i in raw.get('new_chat_members', [])]
        #Optional. New members that were added to the group or supergroup and information about them (the bot itcls may be one of these members)
        cls.left_chat_member: 'User' = User.gen(raw.get('left_chat_member'))
        #Optional. A member was removed from the group, information about them (this member may be the bot itcls)
        cls.new_chat_title: str = raw.get('new_chat_title')
        #Optional. A chat title was changed to this value
        cls.new_chat_photo: list = [PhotoSize.gen(i) for i in raw.get('new_chat_photo', [])]
        #Optional. A chat photo was change to this value
        cls.delete_chat_photo: bool = raw.get('delete_chat_photo', False)
        #Optional. Service message: the chat photo was deleted
        cls.group_chat_created: bool = raw.get('group_chat_created', False)
        #Optional. Service message: the group has been created
        cls.supergroup_chat_created: bool = raw.get('supergroup_chat_created', False)
        #Optional. Service message: the supergroup has been created. This field can't be received in a message coming through updates, because bot can't be a member of a supergroup when it is created. It can only be found in reply_to_message if someone replies to a very first message in a directly created supergroup.
        cls.channel_chat_created: bool = raw.get('channel_chat_created', False)
        #Optional. Service message: the channel has been created. This field can't be received in a message coming through updates, because bot can't be a member of a channel when it is created. It can only be found in reply_to_message if someone replies to a very first message in a channel.
        cls.migrate_to_chat_id: int = raw.get('migrate_to_chat_id') #
        #Optional. The group has been migrated to a supergroup with the specified identifier. This number may be greater than 32 bits and some programming languages may have difficulty/silent defects in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float type are safe for storing this identifier.
        cls.migrate_from_chat_id: int = raw.get('migrate_from_chat_id') #
        #Optional. The supergroup has been migrated from a group with the specified identifier. This number may be greater than 32 bits and some programming languages may have difficulty/silent defects in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float type are safe for storing this identifier.
        cls.pinned_message: 'Message' = Message.gen(raw.get('pinned_message'))
        #Optional. Specified message was pinned. Note that the Message object in this field will not contain further reply_to_message fields even if it is itcls a reply.
        #TODO cls.invoice: 'Invoice' = Invoice
        #Optional. Message is an invoice for a payment, information about the invoice. More about payments »
        #TODO cls.successful_payment'SuccessfulPayment'
        #Optional. Message is a service message about a successful payment, information about the payment. More about payments »
        cls.connected_website: str = raw.get('connected_website')
        #Optional. The domain name of the website on which the user has logged in. More about Telegram Login »
        #TODO passport_data'PassportData'
        #Optional. Telegram Passport data
        cls.reply_markup: 'InlineKeyboardMarkup' = raw.get('reply_markup')
        #Optional. Inline keyboard attached to the message. login_url buttons are represented as ordinary url buttons.
        return cls


class CallbackQuery:
    @classmethod
    def gen(cls, raw):
        if not raw:
            return None
        cls.id: str = raw.get('id')
        #Unique identifier for this query
        cls.from: 'User' = raw.get('from')
        #Sender
        cls.message: 'Message' = raw.get('message')
        #Optional. Message with the callback button that originated the query. Note that message content and message date will not be available if the message is too old
        cls.inline_message_id: str = raw.get('inline_message_id')
        #Optional. Identifier of the message sent via the bot in inline mode, that originated the query.
        cls.chat_instance: str = raw.get('chat_instance')
        #Global identifier, uniquely corresponding to the chat to which the message with the callback button was sent. Useful for high scores in games.
        cls.data: str = raw.get('data')
        #Optional. Data associated with the callback button. Be aware that a bad client can send arbitrary data in this field.
        cls.game_short_name: str = raw.get('game_short_name')
        #Optional. Short name of a Game to be returned, serves as the unique identifier for the game