import sqlite3
import aiosqlite
import os
import asyncio
from datetime import datetime

class ReplyChain:
    table_name = 'messages'

    def __init__(self, path: str, base_name: str, time_to_clean_messages: int):
        self.path = path
        self.base_name = base_name
        self.time_to_clean_messages = time_to_clean_messages
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        if not os.path.isfile(self.path + self.base_name):
            with open(self.path + self.base_name, 'w+'):
                pass
        self.make_db_table()
        

    def make_db_table(self):
        conn = sqlite3.connect(self.path + self.base_name)
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (fromTID INTEGER, fromMID INTEGER, toTID INTEGER, toMID INTEGER, time INTEGER)")
        conn.commit()
        conn.close()

    async def add_data(self, from_tid: int, from_mid: int, to_tid: int, to_mid: int, time: int):
        async with aiosqlite.connect(self.path + self.base_name) as db:
            await db.execute(f"INSERT INTO {self.table_name} VALUES (?,?,?,?,?)", (from_tid, from_mid, to_tid, to_mid, time))
            await db.commit()


    async def get_reply(self, reply_to_message_id: int) -> list:
        res = []
        async with aiosqlite.connect(self.path + self.base_name) as db:
            _ = []
            sql = f"SELECT * FROM {self.table_name} WHERE toMID=?"
            async with db.execute(sql, [(reply_to_message_id)]) as cursor:
                _ = await cursor.fetchone()
            if _:
                sql = f"SELECT * FROM {self.table_name} WHERE fromMID=?"
                async with db.execute(sql, [(_[1])]) as cursor:
                    res = await cursor.fetchmany()
        return res

    async def clear_old(self):
        sql = f'DELETE FROM {self.table_name} WHERE time BETWEEN 0 and ?'
        async with aiosqlite.connect(self.path + self.base_name) as db:
            current_ts = int(datetime.timestamp(datetime.now())) - self.time_to_clean_messages
            await db.execute(sql, (current_ts,))
            await db.commit()