from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import as_list, as_numbered_list#ДЛя красивого парса. разобраться
from ..filters.chat_types import ChatTypeFilter
from ..keyboards import kbd

router_user_private = Router()
router_user_private.message.filter(ChatTypeFilter(['private']))# Разделение роутеров


# @router_user_private.message(F.text.lower() == "start")
@router_user_private.message(or_f(CommandStart(), F.text.lower() == "start"))
async def start_cmd(message: Message):
    await message.answer(text=f"Hi! I\'m a virtual helper. Do you want I help you?", reply_markup=kbd.start_keyboard)#reply_markup - указать клавиатуру на старте


@router_user_private.message(F.text.lower() == "menu")
@router_user_private.message(Command("menu"))
async def menu_cmd(message: Message, bot: Bot):
    # await bot.send_message(message.from_user.id, text='text') - ответ через класс Bot
    await message.answer(text=f"Menu: {message.text}", reply_markup=kbd.start_keyboard_3.as_markup(resize_keyboard=True))#Добавление клавы через Bielder класс


@router_user_private.message(F.text.lower() == "back")
@router_user_private.message(Command("back"))
async def back_cmd(message: Message):
    await message.answer(f"Это команда  {message.text}")


@router_user_private.message(Command("main"))
async def main_cmd(message: Message):
    await message.answer(f"Это команда {message.text}")


# Магические фильтры
@router_user_private.message(F.content_type.in_({'text', 'photo'}))
async def magic_filter(message: Message):
    print(message)
    await message.answer(f"<i>Это</i> <b>магический</b> фильтр текста! Ёпт...")#Форматирование отправляемого текста
