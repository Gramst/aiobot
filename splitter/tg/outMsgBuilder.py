from typing import List, Union, Callable
import asyncio

from .abs_outMsg import AbsFactoryMessages, OutMessage, TextHandler
from .text_handlers import TextHandlerList
from .income_message import InMessage

class DirectorOutMessages:

    def __init__(self):
        self.handlers = TextHandlerList()

    async def make_empty_text_message(self, text_handler: TextHandler = None) -> OutMessage:
        if text_handler and isinstance(text_handler, TextHandler):
            result = AbsFactoryMessages.get_text_message(text_handler)
        else:
            result = AbsFactoryMessages.get_text_message(self.handlers.get_handler(self.handlers.BASE_TEXT))
        result.method_name = 'sendMessage'
        return result

    async def make_auto_message_from_income(self):
        pass
