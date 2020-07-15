import asyncio
from aiohttp import ClientSession

class AIODoRequest:

    @staticmethod
    async def do_request(url: str, parameters: dict) -> dict:
        async with ClientSession() as session:
            async with session.get(url, params=parameters) as resp:
                return await resp.json()
