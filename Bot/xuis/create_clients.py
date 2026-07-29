import os
import uuid
import secrets
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("URL")


async def create_clients(
        session,
        inbound_id,
        tg_id,
        headers,
        expiry_time
):

    client_id = str(uuid.uuid4())

    payload = {
        "client": {
            "id": client_id,
            "email": str(tg_id),
            "auth": secrets.token_urlsafe(12),
            "comment": "",
            "enable": True,
            "flow": "",
            "group": "",
            "password": secrets.token_urlsafe(12),
            "reset": 0,
            "security": "auto",
            "subId": secrets.token_hex(8),
            "totalGB": 0,
            "limitIp": 0,
            "expiryTime": expiry_time,
            "tgId": tg_id
        },
        "inboundIds": [
            inbound_id
        ]
    }

    async with session.post(
        f"{BASE_URL}/panel/api/clients/add",
        json=payload,
        headers=headers
    ) as response:

        text = await response.text()

        print(
            "CREATE STATUS:",
            response.status,
            text
        )

        if response.status != 200:
            raise Exception(text)

    return client_id