import os
from dotenv import load_dotenv

load_dotenv()


BASE_URL = os.getenv("URL")

async def get_inbounds(session):
    async with session.get(f"{BASE_URL}/panel/api/inbounds/list") as resp:
        return await resp.json()