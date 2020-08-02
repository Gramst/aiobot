import asyncio
import json
from aiohttp import ClientSession
from dataclasses import asdict, astuple

class DataToSerialise:

    def get_data(self) -> dict:
        _ = asdict(self)
        return {k: v for k, v in _.items() if v}


class AIODoRequest(DataToSerialise):

    async def do_request(self, base_url: str, chat_id: int) -> dict:
        headers = {
            'Content-Type': 'application/json'
        }
        data = self.get_data()
        data['chat_id'] = chat_id
        print(f'send to {chat_id}')
        async with ClientSession() as session:
            async with session.post(base_url + self.__class__.__name__,
                                    data=json.dumps(data),
                                    headers=headers) as resp:
                res = await resp.json()
                return res
