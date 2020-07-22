from .tg import InMessage, OutMessage

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
                print(await out.method.do_request(self.base_url))