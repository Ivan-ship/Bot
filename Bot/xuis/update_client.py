import os
from dotenv import load_dotenv
from xuis.login import login
from xuis.get_inbounds import get_inbounds

load_dotenv()

BASE_URL = os.getenv("URL")

async def update_client(tg_id: int, expiry_time: int):

    session, headers = await login()

    try:

        data = await get_inbounds(session)

        client = None

        for inbound in data["obj"]:
            for c in inbound["settings"]["clients"]:
                if c["email"] == str(tg_id):
                    client = c
                    break

            if client:
                break

        if client is None:
            raise Exception("Клиент не найден")

        client["expiryTime"] = expiry_time
        client["enable"] = True

        async with session.post(
            f"{BASE_URL}/panel/api/clients/update/{client['email']}",
            json=client,
            headers=headers
        ) as resp:

            print(await resp.text())

    finally:
        await session.close()