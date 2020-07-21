import asyncio
import json
from aiohttp import ClientSession

class AIODoRequest:
    API_URL: str
    
    def get_data(self):
        raise NotImplementedError

    async def do_request(self) -> dict:
        headers = {
            'Content-Type': 'application/json'
        }
        async with ClientSession() as session:
            async with session.post(self.API_URL,
                                    data=json.dumps(self.get_data()),
                                    headers=headers) as resp:
                return resp.json()
