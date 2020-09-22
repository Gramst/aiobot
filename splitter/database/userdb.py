from dataclasses import dataclass, field
import sqlite3
import aiosqlite
import os
import asyncio
import pickle
from typing import List

from ..tg import InMessage
from .userProfile import User


class UsersDBconnect:

    def __init__(self, path: str, base_name: str, table_name: str):
        sqlite3.register_converter("pickle", pickle.loads)
        sqlite3.register_adapter(User, pickle.dumps)
        self.path       = path
        self.base_name  = base_name
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        if not os.path.isfile(self.path + self.base_name):
            with open(self.path + self.base_name, 'w+'):
                pass

        self.SQL_MAKE_TABLE       = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER, user_data pickle, ban INTEGER, active INTEGER)"
        self.SQL_INSERT_USER      = f"INSERT INTO {table_name} VALUES (?,?,?,?)"
        self.SQL_UPDATE_USER      = f"UPDATE {table_name} SET user_data=?, ban=?, active=? WHERE id=?"
        self.SQL_SELECT_USER      = f"SELECT * FROM {table_name} WHERE id=?"
        self.SQL_GET_ACTIVE_USERS = f"SELECT user_data FROM {table_name} WHERE active BETWEEN 1 and 1"

        self.make_db_table()

    def make_db_table(self):
        conn = sqlite3.connect(self.path + self.base_name, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute(self.SQL_MAKE_TABLE)
        conn.commit()
        conn.close()

    async def add_data(self, user: User):
        sql = self.SQL_INSERT_USER
        async with aiosqlite.connect(self.path + self.base_name, detect_types=sqlite3.PARSE_DECLTYPES) as db:
            await db.execute(sql, [(user.chat_id), (user), (user.banned), (user.active)])
            await db.commit()

    async def update_data(self, user: User):
        sql = self.SQL_UPDATE_USER
        async with aiosqlite.connect(self.path + self.base_name, detect_types=sqlite3.PARSE_DECLTYPES) as db:
            await db.execute(sql, (user, user.banned, user.active, user.chat_id))
            await db.commit()

    async def get_data(self, chat_id: int) -> User:
        sql = self.SQL_SELECT_USER
        async with aiosqlite.connect(self.path + self.base_name, detect_types=sqlite3.PARSE_DECLTYPES) as db:
            async with db.execute(sql, [(chat_id)]) as cursor:
                res = await cursor.fetchone()
            return res

    def get_active(self) -> List[User]:
        sql = self.SQL_GET_ACTIVE_USERS
        res = []
        conn = sqlite3.connect(self.path + self.base_name, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute(sql)
        _ = c.fetchall()
        if _:
            res = [i[0] for i in _]
        conn.commit()
        conn.close()
        res = [i for i in res]
        print(res)
        return res

class UsersDB:

    def __init__(self, path: str, base_name: str, table_name: str):
        self.db_api = UsersDBconnect(path, base_name, table_name)
        self.users_list : list = self.db_api.get_active()

    async def get_user(self, chat_id: int) -> User:
        master = None
        _ = [i for i in self.users_list if i.chat_id == chat_id]
        if _:
            master = _[0]
        else:
            master = await self.db_api.get_data(chat_id)                
            if not master:
                master = User(chat_id)
                await self.db_api.add_data(master)
            self.users_list.append(master)
        return master

    async def update_user(self, user: User):
        self.db_api.update_data(user)