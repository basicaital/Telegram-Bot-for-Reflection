from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from .handlers import start_router


class MoodBot:
    def __init__(self, token: str, default: DefaultBotProperties):
        self.bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dp = Dispatcher(storage=MemoryStorage())
        self.dp.include_router(start_router)

    async def start(self):
        await self.dp.start_polling(self.bot)
        await self.bot.delete_webhook(drop_pending_updates=True)
