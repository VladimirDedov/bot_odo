from aiogram import Bot, Dispatcher
from aiogram.types import Message

# Реакция на команду /start
async def get_start(messege: Message, bot: Bot):
    await bot.send_message(messege.from_user.id, f"Здарова {messege.from_user.first_name}, заебал!")
    # Просто отправляет сообщение
    await messege.answer(f"Здарова <b>{messege.from_user.first_name}</b>, заебал!")
    # Отвечает с сылкой на сообщение пользователя
    await messege.reply(f"<tg-spoiler>Здарова {messege.from_user.first_name}, заебал!</tg-spoiler>")