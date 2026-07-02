from datetime import date
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
import os
from sqlalchemy import select
from queries.model import User, Subscribe
from xui import create_user

load_dotenv()


start_date = date.today()


#Create subsriction
async def create_subscription(session, user_id: int, month: int, price: int, plan: str):
    stmt = select(Subscribe).where(
        Subscribe.id == user_id
    )
    result = await session.execute(stmt)
    subscription = result.scalar_one_or_none()

    if subscription is None:

        vless_url = await create_user(user_id, month)

        subscription = Subscribe(
            id = user_id,
            start_date = date.today(),
            end_date = date.today() + relativedelta(months=month),
            url = vless_url,
            price = price,
            plan = plan
        )
        session.add(subscription)
    await session.commit()

    return subscription