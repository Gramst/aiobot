from .tg import InMessage, OutMessage, ResponseMessage
from .database import ReplyChain

from aiohttp import web
import asyncio 
from datetime import datetime

class Splitter:
    jobs: list

    def __init__(self, token: str, bases_path: str):
        self.token = token
        self.base_url: str = f'https://api.telegram.org/bot{self.token}/'
        self.in_queue = asyncio.Queue()
        self.reply_chain = ReplyChain(bases_path, 'reply.db')
        self.jobs = []

    async def income_msg(self, request) -> InMessage:
        data = await request.json()
        self.in_queue.put_nowait(InMessage(data))
        return web.Response(status=200)

    async def kronos(self):
        [i.update_timer() for i in self.jobs]
        _ = [i for i in jobs if i.ready]
        for job in _:
            await job.run()

    async def process(self):
        while True:
            income = await self.in_queue.get()
            if income.message:
                out = OutMessage()
                if income.message.reply_to_message:
                    print(await self.reply_chain.get_reply(income.message.reply_to_message.message_id))
                out << income
                r_msg = await out.send_to_server(self.base_url)
                if r_msg:
                    print(
                        r_msg.from_id,
                        r_msg.from_message_id,
                        r_msg.result.chat.id,
                        r_msg.result.message_id,
                        r_msg.result.date,
                        r_msg.result.date - int(datetime.timestamp(datetime.now()))
                        )
                    await self.reply_chain.add_data(
                        r_msg.from_id,
                        r_msg.from_message_id,
                        r_msg.result.chat.id,
                        r_msg.result.message_id,
                        r_msg.result.date
                        )
