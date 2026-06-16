from datetime import date
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
import os
from sqlalchemy import select
from queries.model import User, Subscribe

load_dotenv()

sub_url = os.getenv("SUBSCRIBE_URL")

start_date = date.today()


#Create subsriction
async def create_subscription(session, user_id: int, month: int, price: int):
    stmt = select(Subscribe).where(
        Subscribe.id == user_id
    )
    result = await session.execute(stmt)
    subscription = result.scalar_one_or_none()

    if subscription is None:
        subscription = Subscribe(
            id = user_id,
            start_date = date.today(),
            end_date = date.today() + relativedelta(months=month),
            url = sub_url,
            price = price
        )
        session.add(subscription)
    await session.commit()

    return subscription