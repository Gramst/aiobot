from dataclasses import dataclass, field

from . import InMessage

@dataclass(init=False)
class OutMessage:
    type            : str
    from_id         : int
    from_message_id : int
    text            : str

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
        if other.message.document.
            