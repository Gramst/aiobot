import asyncio

async def do_request(url: str, parameters: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL + url, params=parameters) as resp:
            return await resp.json()
