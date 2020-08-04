from nanoid import generate

from ..database import User
from .messages  import OutMessage

class Page:
    pass

class Menu:
    menu_id: str
    master: User

    def __init__(self, master):
        self.menu_id = generate(size=8)
        self.master  = master

    def reg_page(self, page: Page):
        pass
