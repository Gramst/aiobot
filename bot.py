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
                data.master.state_user.echo = not data.master.state_user.echo
                out = data.get_out_msg(promt='<service> ::', text=f' echo set to {data.master.state_user.echo}')
                out.set_notify_to_system()
                out.promt_obj.as_bold()
                out.promt_obj.as_italic()
                out.as_text()
                out.add_destination(data.master)
                data.out_que.put_nowait(out)
                return True

        out = data.get_out_msg()
        out.set_notify_to_normal()
        out.promt = data.master.nick
        out.promt_obj.as_bold()
        out.text_obj.as_italic()
        out << data.in_msg
        await out.get_reply_block()
        if data.master.state_user.echo:
            [out.add_destination(i) for i in data.users]
        else:
            [out.add_destination(i) for i in data.users if i.chat_id != data.master.chat_id]
        data.out_que.put_nowait(out)
        return True

    return False
