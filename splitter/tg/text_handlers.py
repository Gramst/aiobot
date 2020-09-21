from .abs_outMsg import TextHandler, TextPreSet

class TextHandlerList:
    BASE_TEXT  = "__b_text"
    BASE_PHOTO = "__b_photo"

    handlers: dict = {}

    def __init__(self):
        self.handlers[self.BASE_TEXT]  = self.__get_base_text_h()
        self.handlers[self.BASE_PHOTO] = self.__get_base_photo_h()

    def registry_handler(self, name: str, handler: TextHandler):
        self.handlers[name] = handler

    def get_handler(self, name: str) -> TextHandler:
        self.handlers.get(name, None)

    def get_tiny_handler_text(self, text_f_str: str) -> TextHandler:
        _ = TextPreSet(text_f_str)
        _.text_format_list[_.MASTER].as_bold()
        _.text_format_list[_.SLAVE].as_bold()
        _.text_format_list[_.OTHER].as_bold()    
        _.text_format_list[_.TEXT].as_italic()
        return TextHandler(_, _, _)

    def __get_base_photo_h(self) -> TextHandler:
        mm = TextPreSet('{file_id}\n{master}\n{slave}')
        m = TextPreSet('{text}')
        m.text_format_list[m.TEXT].as_italic()
        return TextHandler(mm, m, m)
    
    def __get_base_text_h(self) -> TextHandler:
        mm = TextPreSet('{master}\n{slave}\n{text}')
        m  = TextPreSet('{master}{custom}{text}', ' : ')
        m.text_format_list[m.MASTER].as_bold()
        m.text_format_list[m.TEXT].as_italic()
        return TextHandler(mm, m, m)