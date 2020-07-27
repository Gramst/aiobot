from dataclasses import dataclass
import sqlite3
import aiosqlite
import os
import asyncio
import pickle
from typing import List


class User:
    chat_id : int
    banned  : int
    active  : int
    f_new   : bool
    
    
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.banned  = 0
        self.active  = 1
        self.f_new   = True


class UsersDB:
    table_name = 'users'

    def __init__(self, path: str, base_name: str):
        sqlite3.register_converter("pickle", pickle.loads)
        sqlite3.register_adapter(User, pickle.dumps)
        self.path = path
        self.base_name = base_name
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        if not os.path.isfile(self.path + self.base_name):
            with open(self.path + self.base_name, 'w+'):
                pass
        self.make_db_table()
        

    def make_db_table(self):
        conn = sqlite3.connect(self.path + self.base_name)
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER, user_data BLOB, ban INTEGER, active INTEGER)")
        conn.commit()
        conn.close()

    async def add_data(self, user: User):
        async with aiosqlite.connect(self.path + self.base_name) as db:
            await db.execute(f"INSERT INTO {self.table_name} VALUES (?,?,?,?)", (user.chat_id, user, user.banned, user.active))
            await db.commit()


    async def get_data(self, chat_id: int) -> User:
        async with aiosqlite.connect(self.path + self.base_name) as db:
            sql = f"SELECT * FROM {self.table_name} WHERE id=?"
            async with db.execute(sql, [(chat_id)]) as cursor:
                res = await cursor.fetchone()
            if res:
                return res[1]
            else:
                return User(chat_id)

    async def get_active(self) -> List[User]:
        res = []
        async with aiosqlite.connect(self.path + self.base_name) as db:
            sql = f"SELECT user_data FROM {self.table_name} WHERE active BETWEEN 1 and 1"
            async with db.execute(sql) as cursor:
                res = await cursor.fetchmany()
        return res
