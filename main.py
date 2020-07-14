import asyncio
import aiohttp
from aiohttp import web
import json
import ssl

from nonpublic import TOKEN, CRT, KEY
from bot.tgmessage import Message, CallbackQuery

API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
sslcontext.load_cert_chain(CRT,keyfile=KEY)

class BotHandler:
    
    def __init__(self, in_message_queue: 'asyncio.queue', out_msg_queue):
       self.in_message_queue = in_message_queue
       self.out_message_queue = out_msg_queue

    async def income_msg(self, request):
        data = await request.json()
        self.in_message_queue.put_nowait(data)
        return web.Response(status=200)

async def init_app(loop, handler):
    app = web.Application(loop=loop, middlewares=[])
    app.router.add_post(f'/{TOKEN}', handler)
    return app

async def process(in_msg_queue, out_msg_queue):
    while True:
        data = await in_msg_queue.get()
        in_msg_queue.task_done()
        income = Message.gen(data.get('message'))
        if not income:
            income = CallbackQuery.gen(data.get('callback_query'))
        if isinstance(income, Message):
            message = {
                'chat_id': income.chat.id,
                'text': income.text,
            }
            print(message)
            out_msg_queue.put_nowait(message)
        

async def send_f(out_queue):
    while True:
        message = await out_queue.get()
        headers = {
            'Content-Type': 'application/json'
        }
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.post(API_URL,
                                    data=json.dumps(message),
                                    headers=headers) as resp:
                try:
                    assert resp.status == 200
                except:
                    print('Send not ok')
        print('Send ok')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    in_msg_queue = asyncio.Queue()
    out_msg_queue = asyncio.Queue()
    time_task = loop.create_task(process(in_msg_queue, out_msg_queue))
    send_task = loop.create_task(send_f(out_msg_queue))
    handler = BotHandler(in_msg_queue, out_msg_queue)
    try:
        app = loop.run_until_complete(init_app(loop, handler.income_msg))
        web.run_app(app, host='0.0.0.0', port=8443, ssl_context=sslcontext)
    except Exception as e:
        print('Error create server: %r' % e)
    finally:
        pass
    loop.close()
