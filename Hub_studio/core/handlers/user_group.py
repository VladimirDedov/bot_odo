from string import punctuation  # Строка со всемии знаками пунктуации
from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from ..config import restricted_words
from ..filters.chat_types import ChatTypeFilter

router_user_group = Router()
router_user_group.message.filter(ChatTypeFilter(['group', 'supergroup']))  # Разделение роутеров


def clean_text(text: str):  # очистка строки от знаков пунктуации
    return text.translate(str.maketrans('', '', punctuation))


@router_user_group.message(Command('admin'))
async def get_admins(message: Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    admins_list = [#Генератор по добалению админов в список
        member.user.id
        for member in admins_list
        if member.status in ('creator', 'administartor')
    ]
    bot.my_admin_list = admins_list[:]
    print(bot.my_admin_list)
    if message.from_user.id in admins_list:
        await message.delete()


@router_user_group.edited_message()
@router_user_group.message()
async def cleaner(message: Message):
    if restricted_words.intersection(clean_text(
            message.text.lower()).split()):  # Сравниваем множества на пересечение restrict и созданное множество из текста
        await message.answer(f"{message.from_user.first_name}, соблюдайте правила!")
        await message.delete()

# Хэндлеры машины состояния
