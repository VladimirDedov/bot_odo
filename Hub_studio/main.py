import asyncio
import os
import core.config as config

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

from core.middlewares.db import DataBaseSession
from core.handlers.user_private import router_user_private
from core.handlers.user_group import router_user_group
from core.handlers.admin_private import admin_router
from core.database.engine import create_db, session_maker

bot = Bot(token=os.getenv("TOKEN"),
          parse_mode=ParseMode.HTML)  # Форматирование отправляемого текста)  # TOKEN - считывается из виртуального окружения
bot.my_admin_list = []
dp = Dispatcher()
dp.include_routers(admin_router, router_user_private, router_user_group)  # Подключение роутера к боту


async def main():
    await create_db()
    # Мидлваре после прохождения всех фильтров на любое действие
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    # Bot не отвечает на сообщения, которые пришли, когда он не работал.
    await bot.delete_webhook(drop_pending_updates=True)
    # Добавление меню программно
    await bot.set_my_commands(commands=config.chat_private_menu, scope=types.BotCommandScopeAllPrivateChats())
    # Запуск бота на прослущивание сервера телеграмм. allowed_updates - то, что хотим приходило с сервера телеги
    await dp.start_polling(bot, allowed_updates=config.ALLOWED_UPDATES)


if __name__ == "__main__":
    asyncio.run(main())
