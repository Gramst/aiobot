import sqlite3
import aiosqlite
import os
import asyncio

class ReplyChain:

    def __init__(self, path, base_name):
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
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='stocks' ''')
        if c.fetchone()[0]==1:
            pass
        else:
            c.execute('''CREATE TABLE stocks
                (fromTID INTEGER, fromMID INTEGER, toTID INTEGER, toMID INTEGER, time INTEGER)''')
        conn.commit()
        conn.close()

    async def add_data(self, from_tid: int, from_mid: int, to_tid: int, to_mid: int, time: int):
        async with aiosqlite.connect(self.path + self.base_name) as db:
            await db.execute("INSERT INTO stocks VALUES (?,?,?,?,?)", (from_tid, from_mid, to_tid, to_mid, time))
            await db.commit()


    async def get_reply(self, reply_to_message_id: int) -> list:
        res = []
        async with aiosqlite.connect(self.path + self.base_name) as db:
            _ = []
            sql = "SELECT * FROM stocks WHERE toMID=?"
            async with db.execute(sql, [(reply_to_message_id)]) as cursor:
                _ = await cursor.fetchone()
            if _:
                sql = "SELECT * FROM stocks WHERE fromMID=?"
                async with db.execute(sql, [(_[1])]) as cursor:
                    res = await cursor.fetchmany()
        return res

    async def clear_old(self, timestamp_oldest: int):
        sql = 'DELETE FROM stocks WHERE time BETWEEN 0 and ?'
        async with aiosqlite.connect(self.path + self.base_name) as db:
            await db.execute(sql, (timestamp_oldest))
            await db.commit()
            #(int(datetime.timestamp(datetime.now())))