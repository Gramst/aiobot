from nanoid import generate
from typing import List

from ..database import User
from .messages  import OutMessage

class MenuButton:
    legend: str
    action

class Page:
    page_name: str
    buttons  : List[MenuButton]

    def gen_msg(self):
        pass


class Menu:
    menu_id    : str
    state      : str
    master     : User
    pages      : List[Page]

    def __init__(self, master):
        self.menu_id = generate(size=8)
        self.master  = master
        self.state   = 'main'

    def main_page(self):
        pg = [i for i in self.pages if i.page_name = 'main']
        if pg:
            pg = pg.pop()

        msg = pg.gen_msg()