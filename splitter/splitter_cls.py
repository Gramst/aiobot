from aiohttp import web
import asyncio 
from datetime import datetime
from typing import List
from functools import wraps
from dataclasses import dataclass

from .tg import InMessage, DirectorOutMessages, AbsFactoryMessages
from .tg.telegramclasses.t_methods import answerCallbackQuery
from .database import ReplyChain, User, UsersDB
from .jobs import Job

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class CoreSingleton:
    clean_messages_older: int = 86400
    tic_delay           : int = 5
    jobs                : List[Job]

    def __init__(self):
        self.jobs    = []
        self.token   = ''
        self.in_queue  = asyncio.Queue()
        self.out_queue = asyncio.Queue()
        self.user_database = None
        self.outMesageBilder = DirectorOutMessages()
        self.message_database = None
        self.base_url = None

    def set(self, token: str, base_path: str):
        self.token   = token
        self.base_url = f'https://api.telegram.org/bot{self.token}/'
        self.user_database = UsersDB(base_path, 'reply.db', 'users')
        self.message_database = ReplyChain(base_path, 'reply.db', self.clean_messages_older)
        self.jobs.append(Job.get_job(self.message_database.clear_old, 25))
        self.jobs.append(Job.get_job(self._user_update, 5))

    def set_bot_logic(self, logic_function):
        self.bot_logic = logic_function

    async def _user_update(self):
        [i.update() for i in self.user_database.users_list if i]

    async def income_msg(self, request) -> InMessage:
        data = await request.json()
        income = InMessage(data)
        if income.callback:
            master_id = income.callback.from_u.id
        elif income.message:
            master_id = income.message.chat.id
        master = await self.user_database.get_user(master_id)
        if income.message and income.message.reply_to_message:
            slave_id = self.message_database.get_id_from_reply(income.message.reply_to_message_id.message_id)
            if slave_id:
                slave = await self.user_database.get_user(slave_id)
        print(master, '\n',  slave)
        await self.user_database.update_user(master)
        if slave:
            await self.user_database.update_user(slave)
        return web.Response(status=200)

    async def kronos(self):
        while True:
            [i.update_timer() for i in self.jobs]
            _ = [i for i in self.jobs if i.is_ready]
            for job in _:
                await job.run()
            await asyncio.sleep(self.tic_delay)
