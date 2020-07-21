import asyncio
import aiohttp
from aiohttp import web
import json
import ssl

from nonpublic import TOKEN, CRT, KEY
from tg.messages import InMessage, OutMessage

API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
sslcontext.load_cert_chain(CRT,keyfile=KEY)

class BotHandler:
    
    def __init__(self, in_message_queue: 'asyncio.queue', out_msg_queue):
       self.in_message_queue = in_message_queue
       self.out_message_queue = out_msg_queue

    async def income_msg(self, request):
        data = await request.json()
        msg = InMessage(data)
        if msg.not_empty:
            self.in_message_queue.put_nowait(msg)
        return web.Response(status=200)

async def init_app(loop, handler):
    app = web.Application(loop=loop, middlewares=[])
    app.router.add_post(f'/{TOKEN}', handler)
    return app

async def process(in_msg_queue, out_msg_queue):
    while True:
        income = await in_msg_queue.get()
        if income.message:
            out = OutMessage()
            out << income
            res = await out.send_to()
            print(res)
            # message = {
            #     'chat_id': income.message.chat.id,
            #     'text': income.message.from_u.first_name + ' : ' + income.message.text,
            # }
            # out_msg_queue.put_nowait(message)
        

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
                    #return resp.json()
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
