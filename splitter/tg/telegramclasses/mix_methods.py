import asyncio
import json
from aiohttp import ClientSession
from dataclasses import asdict, astuple

class DataToSerialise:

    def get_data(self):
        _ = asdict(self)
        return {k: v for k, v in _.items() if v}


class AIODoRequest(DataToSerialise):

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
