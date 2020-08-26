import asyncio
import json
from aiohttp import ClientSession
from dataclasses import asdict, astuple

class DataToSerialise:

    def get_data(self) -> dict:
        _ = asdict(self)
        return {k: v for k, v in _.items() if v}


class AIODoRequest(DataToSerialise):

    async def do_request(self, base_url: str, chat_id: int = None) -> dict:
        headers = {
            'Content-Type': 'application/json'
        }
        data = self.get_data()
        if chat_id:
            data['chat_id'] = chat_id
            reply_val = data.get('reply_to_message_id')
            print(f'send to {chat_id} reply to {reply_val}')
        async with ClientSession() as session:
            async with session.post(base_url + self.__class__.__name__,
                                    data=json.dumps(data),
                                    headers=headers) as resp:
                res = await resp.json()
                return res
