import asyncio
import json
from aiohttp import ClientSession
from dataclasses import asdict, astuple


class AIODoRequest:
    
    def get_data(self):
        raise NotImplementedError

    async def do_request(self, base_url) -> dict:
        headers = {
            'Content-Type': 'application/json'
        }
        async with ClientSession() as session:
            async with session.post(base_url + self.__class__.__name__,
                                    data=json.dumps(self.get_data()),
                                    headers=headers) as resp:
                res = await resp.json()
                return res

class DataToSerialise:

    def get_data(self):
        _ = astuple(self)
        return dict([ i for i in _ if i])

