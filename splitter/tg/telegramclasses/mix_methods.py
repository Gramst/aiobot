import asyncio
import json
from aiohttp import ClientSession

class AIODoRequest:
    tg_method_name = ''
    
    def get_data(self):
        raise NotImplementedError

    async def do_request(self, base_url) -> dict:
        headers = {
            'Content-Type': 'application/json'
        }
        async with ClientSession() as session:
            async with session.post(base_url + self.tg_method_name,
                                    data=json.dumps(self.get_data()),
                                    headers=headers) as resp:
                res = await resp.json()
                return res
