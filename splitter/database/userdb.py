from dataclasses import dataclass, field
import sqlite3
import aiosqlite
import os
import asyncio
import pickle
from typing import List

from .mix_db import gen_random_nick

VER = 9

@dataclass
class UserData:
    chat_id  : int
    banned   : int  = 0
    active   : int  = 1
    f_new    : bool = True
    nick     : str  = field(init=False)
    tick     : int  = 0
    f_ch_nick: bool = False

    def __post__init__(self):
        self.nick    = gen_random_nick()

class User(UserData):
    
    def __init__(self, chat_id):
        super().__init__(chat_id)

    @classmethod
    def check_version(cls, other: 'User') -> 'User':
        other_version = getattr(other, 'VERSION', 0)
        if VER == other_version:
            print('Version check OK')
            return other
        print(f'Update User from {other_version} to {VER}')
        res = cls(other.chat_id)
        res.banned = getattr(other, 'banned', 0)
        res.active = getattr(other, 'active', 1)
        res.nick   = getattr(other, 'nick', gen_random_nick())
        res.tick   = getattr(other, 'tick', 0)
        return res

    def update(self):
        self.tick += 1


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
        conn = sqlite3.connect(self.path + self.base_name, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER, user_data pickle, ban INTEGER, active INTEGER)")
        conn.commit()
        conn.close()


    async def add_data(self, user: User):
        sql = f"INSERT INTO {self.table_name} VALUES (?,?,?,?)"
        async with aiosqlite.connect(self.path + self.base_name, detect_types=sqlite3.PARSE_DECLTYPES) as db:
            await db.execute(sql, [(user.chat_id), (user), (user.banned), (user.active)])
            await db.commit()

    async def update_data(self, user: User):
        sql = f"UPDATE {self.table_name} SET user_data=?, ban=?, active=? WHERE id=?"
        async with aiosqlite.connect(self.path + self.base_name, detect_types=sqlite3.PARSE_DECLTYPES) as db:
            await db.execute(sql, (user, user.banned, user.active, user.chat_id))
            await db.commit()


    async def get_data(self, chat_id: int) -> User:
        sql = f"SELECT * FROM {self.table_name} WHERE id=?"
        async with aiosqlite.connect(self.path + self.base_name, detect_types=sqlite3.PARSE_DECLTYPES) as db:
            async with db.execute(sql, [(chat_id)]) as cursor:
                res = await cursor.fetchone()
            if res:
                return User.check_version(res[1])
            else:
                return None

    def get_active(self) -> List[User]:
        sql = f"SELECT user_data FROM {self.table_name} WHERE active BETWEEN 1 and 1"
        res = []
        conn = sqlite3.connect(self.path + self.base_name, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute(sql)
        _ = c.fetchall()
        if _:
            res = [i[0] for i in _]
        conn.commit()
        conn.close()
        res = [User.check_version(i) for i in res]
        print(res)
        return res
