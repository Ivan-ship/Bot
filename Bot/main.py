import asyncio
import logging
import os
import sys
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handler.start_handler import router as start_router
from handlers import router as subscribe_router
from queries.database import create_tables
from shelduler.notify import subscribe_worker

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(subscribe_router)
dp.include_router(start_router)

dp["max_updates_in_flight"] = 1



async def main():
    logging.basicConfig(level=logging.INFO)
    await create_tables()

    worker_task = asyncio.create_task(subscribe_worker(bot))
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
         pass
    finally:
         worker_task.cancel()
         
    await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
         print("Bot stopped")