from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
import os
from sqlalchemy import select, update
from queries.model import User, Subscribe
from xuis.create_user import create_user
from xuis.update_client import update_client

load_dotenv()


#Create subsriction
async def create_subscription(session, user_id: int, month: int, price: int, plan: str):
    stmt = select(Subscribe).where(
        Subscribe.id == user_id
    )
    result = await session.execute(stmt)
    subscription = result.scalar_one_or_none()

    start_date = date.today()
    end_date = start_date + relativedelta(months=month)

    if subscription is None:
        vless_url = await create_user(user_id, month)

        subscription = Subscribe(
            id = user_id,
            start_date = start_date,
            end_date = end_date,
            url = vless_url,
            price = price,
            plan = plan,
            is_active = True
        )
        session.add(subscription)
    else:
        subscription.start_date = start_date
        subscription.end_date = end_date
        subscription.plan = plan
        subscription.price = price
        subscription.is_active = True
        
        
        expiry_time = int(datetime.combine(end_date, datetime.min.time()).timestamp() * 1000)

        await update_client(tg_id=user_id, expiry_time=expiry_time)
        
    await session.commit()
    await session.refresh(subscription)

    return subscription