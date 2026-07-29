import os
from dotenv import load_dotenv
from xuis.login import login
from xuis.create_clients import create_clients
from xuis.get_inbounds import get_inbounds
from xuis.generate_vless import generate_vless_url
from datetime import datetime
from dateutil.relativedelta import relativedelta

load_dotenv()
BASE_URL = os.getenv("URL")


async def create_user(tg_id: int, month: int):

    session, headers = await login()

    try:
        data = await get_inbounds(session)

        inbound = data["obj"][0]

        expiry = int(
            (datetime.today() + relativedelta(months=month)).timestamp() * 1000
        )

        client_id = await create_clients(
            session=session,
            inbound_id=inbound["id"],
            headers=headers,
            tg_id=tg_id,
            expiry_time=expiry
        )

        profile = {
            "client_id": client_id,
            "remark": inbound["remark"]
        }

        return await generate_vless_url(profile, inbound)

    finally:
        await session.close()