import sqlite3
import aiosqlite

class ReplyChain:

    def __init__(self, path, base_name):
        self.path = path
        self.base_name = base_name
        conn = sqlite3.connect(self.path + base_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE stocks
             (fromTID INTEGER, fromMID INTEGER, toTID INTEGER, toMID INTEGER, time INTEGER)''')
        conn.commit()
        conn.close()