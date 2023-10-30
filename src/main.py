import asyncio
import logging
import sys
from handlers import router
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode 
from os import getenv
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.chat_action import ChatActionMiddleware

async def main() -> None:
    bot = Bot(getenv('BOT_TOKEN'), parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    dp.message.middleware(ChatActionMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())