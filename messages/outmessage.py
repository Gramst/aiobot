from dataclasses import dataclass, field
from typing import List

from . import InMessage

@dataclass(init=False)
class OutMessage:
    type            : str
    from_id         : int
    from_message_id : int
    text            : str
    file_id         : List[str]

    def __init__(self):
        pass

    def __lshift__(self, other: InMessage) -> None:
        if not isinstance(other, InMessage):
            return

        self.from_id = other.message.from_u.id
        self.from_message_id = other.message.message_id
        if other.message.text:
            self.type    = 'text'
            self.text = other.message.text
        if other.message.photo:
            self.type = 'photo'
            self.text = other.message.caption
            self.file_id = [i.file_id for i in other.message.photo]
        if other.message.audio:
            self.type = 'audio'
            self.text = other.message.caption
            self.file_id = [other.message.audio.file_id]
        if other.message.sticker:
            self.type = 'sticker'
            self.file_id = other.message.sticker.file_id
            