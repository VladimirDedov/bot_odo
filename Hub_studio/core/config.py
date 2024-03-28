from dotenv import find_dotenv, load_dotenv
from aiogram.types import BotCommand

ALLOWED_UPDATES = ['message, edited_message']  # ограничение типов апдейтов, которые приходят к боту
load_dotenv(find_dotenv())  # Загружает переменные из .env в окружение os автоматически

chat_private_menu = [
    BotCommand(command='start', description='Начать работу'),
    BotCommand(command='menu', description='Показать меню'),
    BotCommand(command='back', description='Вернуться назад'),
    BotCommand(command='main', description='Вернуться в самое начало')
]

restricted_words = {'стерва', 'мат', 'хомяк', 'коза'}