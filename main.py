import asyncio
import aiohttp
from aiohttp import web
import json
import ssl

from nonpublic import TOKEN, CRT, KEY

from splitter import CoreSingleton

from bot import process_message

sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
sslcontext.load_cert_chain(CRT,keyfile=KEY)

bot = CoreSingleton()
bot.set(TOKEN, 'bratishkabot/')

bot.set_bot_logic(process_message)

async def init_app(loop, bot: CoreSingleton):
    app = web.Application(loop=loop)
    app.router.add_post(f'/{bot.token}', bot.income_msg)
    return app

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    main_task = loop.create_task(bot.process())
    kronos_task = loop.create_task(bot.kronos())
    send_task = loop.create_task(bot.send_out())
    try:
        app = loop.run_until_complete(init_app(loop, bot))
        web.run_app(app, host='0.0.0.0', port=8443, ssl_context=sslcontext)
    except Exception as e:
        print('Error create server: %r' % e)
    finally:
        pass
    loop.close()
