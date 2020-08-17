from aiohttp import web
import asyncio 
from datetime import datetime
from typing import List

from .tg import InMessage, OutMessage, ResponseMessage, Menu
from .tg.telegramclasses.t_methods import answerCallbackQuery
from .database import ReplyChain, User, UsersDB
from .jobs import Job

class Splitter:
    clean_messages_older: int = 86400
    tic_delay           : int = 5
    jobs                : List[Job]
    users_list          : List[User]
    menu_list           : List[Menu]

    def __init__(self, token: str, bases_path: str):
        self.jobs = []
        self.token = token
        self.in_queue = asyncio.Queue()
        self.out_queue = asyncio.Queue()
        self.user_database = UsersDB(bases_path, 'reply.db')
        self.users_list = self.user_database.get_active()
        self.out_message = OutMessage
        self.message_database = ReplyChain(bases_path, 'reply.db', self.clean_messages_older)
        self.out_message.db = self.message_database
        self.base_url = f'https://api.telegram.org/bot{self.token}/'
        self.out_message.base_url = self.base_url
        self.jobs.append(Job.get_job(self.message_database.clear_old, 25))
        self.jobs.append(Job.get_job(self._user_update, 5))

    async def _user_update(self):
        [i.update() for i in self.users_list if i]

    async def income_msg(self, request) -> InMessage:
        data = await request.json()
        self.in_queue.put_nowait(InMessage(data))
        return web.Response(status=200)

    async def send_out(self):
        while True:
            out: OutMessage = await self.out_queue.get()
            await out.send_to_server()

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
            master = await self.get_master_user(income)
            slave  = await self.get_slave_user(income)
            print(master, '\n',  slave)

            if income.callback:
                await answerCallbackQuery(income.callback.id, 'Oh, you touch my talala').do_request(self.base_url, 0)

            if master and not income.callback:
                out = self.out_message()
                out.promt = master.nick
                out << income
                await out.get_reply_block()
                out.set_destination([i.chat_id for i in self.users_list]) # if i.chat_id != master.chat_id]
                self.out_queue.put_nowait(out)
                await self.user_database.update_data(master)

    async def get_master_user(self, income: InMessage) -> User:
        master = None
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
        return master

    async def get_slave_user(self, income: InMessage) -> User:
        slave = None
        if income.message:
            slave_id = None
            if income.message.reply_to_message:
                slave_id = await self.message_database.get_id_from_reply(income.message.reply_to_message.message_id)
                print(slave_id)
            if slave_id:
                _ = [i for i in self.users_list if i.chat_id == slave_id]
                if _:
                    slave = _[0]
                else:
                    slave = await self.user_database.get_data(slave_id)                
                    if not slave:
                        return None
        return slave
