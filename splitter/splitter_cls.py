from aiohttp import web
import asyncio 
from datetime import datetime
from typing import List

from .tg import InMessage, OutMessage, ResponseMessage
from .database import ReplyChain, User, UsersDB
from .jobs import Job

class Splitter:
    clean_messages_older: int = 86400
    tic_delay           : int = 5
    jobs                : list
    users_list          : List[User]

    def __init__(self, token: str, bases_path: str):
        self.jobs = []
        self.token = token
        #self.base_url: str = f'https://api.telegram.org/bot{self.token}/'
        self.in_queue = asyncio.Queue()
        self.out_queue = asyncio.Queue()
        #self.reply_chain = ReplyChain(bases_path, 'reply.db', self.clean_messages_older)
        self.user_database = UsersDB(bases_path, 'reply.db')
        self.users_list = []
        self.out_message = OutMessage
        self.out_message.db = ReplyChain(bases_path, 'reply.db', self.clean_messages_older)
        self.out_message.base_url = f'https://api.telegram.org/bot{self.token}/'
        self.jobs.append(Job.get_job(self.out_message.db.clear_old, 25))

    async def income_msg(self, request) -> InMessage:
        data = await request.json()
        self.in_queue.put_nowait(InMessage(data))
        return web.Response(status=200)

    async def send_out(self):
        while True:
            out: OutMessage = await self.out_queue.get()
            await out.send_to_server(out.from_id)


    async def kronos(self):
        while True:
            [i.update_timer() for i in self.jobs]
            _ = [i for i in self.jobs if i.is_ready]
            for job in _:
                await job.run()
            await asyncio.sleep(self.tic_delay)

    async def process(self):
        while True:
            income = await self.in_queue.get()
            if income.message:
                _ = [i for i in self.users_list if i.chat_id == income.message.chat.id]
                if _:
                    master = _[0]
                else:
                    master = await self.user_database.get_data(income.message.chat.id)                
                    if not master:
                        master = User(income.message.chat.id)
                        await self.user_database.add_data(master)
                    self.users_list.append(master)

                print(master)

                out = self.out_message()
                out.promt = master.nick + ' : '
                out << income
                
                self.out_queue.put_nowait(out)

                await self.user_database.update_data(master)
