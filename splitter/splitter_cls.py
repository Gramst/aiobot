from .tg import InMessage, OutMessage, ResponseMessage

from aiohttp import web
import asyncio 

class Splitter:

    def __init__(self, token: str):
        self.token = token
        self.base_url: str = f'https://api.telegram.org/bot{self.token}/'
        self.in_queue = asyncio.Queue()

    async def income_msg(self, request) -> InMessage:
        data = await request.json()
        self.in_queue.put_nowait(InMessage(data))
        return web.Response(status=200)

    async def process(self):
        while True:
            income = await self.in_queue.get()
            if income.message:
                out = OutMessage()
                out << income
                r_msg = await out.send_to_server(self.base_url)
                if r_msg:
                    print(
                        r_msg.from_id,
                        r_msg.from_message_id,
                        r_msg.result.chat.id,
                        r_msg.result.message_id,
                        r_msg.result.date
                        )
