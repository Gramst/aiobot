import asyncio
import aiohttp
from aiohttp import web
import json
import ssl

from nonpublic import TOKEN, CRT, KEY

from splitter import Splitter

sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
sslcontext.load_cert_chain(CRT,keyfile=KEY)

bot = Splitter(TOKEN)

async def init_app(loop, bot: Splitter):
    app = web.Application(loop=loop)
    app.router.add_post(f'/{bot.token}', bot.income_msg)
    return app

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    time_task = loop.create_task(bot.process())
    try:
        app = loop.run_until_complete(init_app(loop, bot))
        web.run_app(app, host='0.0.0.0', port=8443, ssl_context=sslcontext)
    except Exception as e:
        print('Error create server: %r' % e)
    finally:
        pass
    loop.close()
