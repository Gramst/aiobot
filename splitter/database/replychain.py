import sqlite3
import aiosqlite
import os

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
        c.execute('''CREATE TABLE stocks
            (fromTID INTEGER, fromMID INTEGER, toTID INTEGER, toMID INTEGER, time INTEGER)''')
        conn.commit()
        conn.close()
