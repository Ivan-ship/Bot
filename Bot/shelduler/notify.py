import asyncio
from datetime import date
from sqlalchemy import select
from aiogram import Bot
from queries.database import SessionLocal
from queries.model import Subscribe

#Function notify
async def check_subscription(bot: Bot):
    async with SessionLocal() as session:
       result = await session.execute(select(Subscribe))
       subscriptions = result.scalars().all()
       
       today = date.today()
       
       for sub in subscriptions:
           days_left = (sub.end_date - today).days
           
           if days_left == 3:
               await bot.send_message(sub.id, "⏳ До окончания подписки осталось 3 дня.") 
            
           elif days_left == 2:
               await bot.send_message(sub.id, "⏳ До окончания подписки осталось 2 дня.")
            
           elif days_left == 1:
               await bot.send_message(sub.id, "⚠️ До окончания подписки остался 1 день.")
            
           elif days_left == 0:
               await bot.send_message(sub.id, "❌ Сегодня заканчивается срок действия вашей подписки.")

async def subscribe_worker(bot: Bot):
    while True:
        await check_subscription(bot)
        await asyncio.sleep(60 * 60 * 24)