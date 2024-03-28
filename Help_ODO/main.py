from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
import asyncio
import logging
from core.handlers.basic import get_start
from core.settings import settings


async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text="Бот стартанул!")


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text="Бот тормазнул!")


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                                "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )#логирование
    bot = Bot(token=settings.bots.bot_token, parse_mode="HTML")  # Создаем бота. parse_mode - для редактирования текста. Можно писать в html тегах
    dp = Dispatcher()  # Объект занимается получением апдейтов
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_start)  # Регистрируем Хэндлер
    try:
        await dp.start_polling(bot)  # запуск бесконечного опроса сервера на наличие новых сообщений
    finally:
        await bot.session.close()  # Закрытие сессии бота

if __name__ == "__main__":
    asyncio.run(start())
