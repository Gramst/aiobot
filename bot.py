import asyncio

from splitter import IterationData
from splitter.tg.telegramclasses.t_methods import answerCallbackQuery

async def process_message(data: IterationData) -> bool:
    if data.in_msg.callback:
        await answerCallbackQuery(data.in_msg.callback.id, 'Oh, you touch my talala').do_request(data.base_url, 0)
        return True

    if data.master and not data.in_msg.callback:
        if data.in_msg.message.text:
            if data.in_msg.message.text == '/echo':
                data.master.f_echo = not data.master.f_echo
                out = data.out_msg(promt='<service> ::', text=f' echo set to {data.master.f_echo}')
                out._promt.as_bold()
                out._promt.as_italic()
                out.as_text()
                out.set_destination([data.master.chat_id])
                data.out_que.put_nowait(out)
                return True

        out = data.out_msg()
        out.promt = data.master.nick
        out._promt.as_bold()
        out._text.as_italic()
        out << data.in_msg
        await out.get_reply_block()
        dest = []
        if data.master.f_echo:
            dest = [i.chat_id for i in data.users]
        else:
            dest = [i.chat_id for i in data.users if i.chat_id != data.master.chat_id]
        out.set_destination(dest)
        data.out_que.put_nowait(out)
        return True

    return False
