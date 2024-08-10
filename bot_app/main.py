import asyncio
import logging

from bot.bot import MoodBot
from config import Config
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties


async def main():
    bot = MoodBot(token=Config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
