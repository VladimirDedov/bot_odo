from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(  # Функция формирования клавиатур
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        size: tuple = (2,)
):
    keyboard = ReplyKeyboardBuilder()
    for index, text in enumerate(btns, start=0):
        if request_contact and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*size).as_markup(resize_keyboard=True, input_field_placeholder=placeholder)


start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='start'),
            KeyboardButton(text='menu'),

        ],
        [
            KeyboardButton(text='back'),
            KeyboardButton(text='main'),
        ]
    ],
    resize_keyboard=True,
)

del_keyboard = ReplyKeyboardRemove()

start_keyboard_2 = ReplyKeyboardBuilder()
start_keyboard_2.add(
    KeyboardButton(text='start'),
    KeyboardButton(text='menu'),
    KeyboardButton(text='back'),
    KeyboardButton(text='main'),
)
start_keyboard_2.adjust(2, 2)  # Сколько кнопок в каком ряду

start_keyboard_3 = ReplyKeyboardBuilder()
start_keyboard_3.attach(start_keyboard_2)
start_keyboard_3.row(  # Добавит кнопку новым рядом
    KeyboardButton(text='Add'),
)
start_keyboard_3.adjust(2, 2)  # Сколько кнопок в каком ряду

ADMIN_KB = get_keyboard(
    "Добавить проблему",
    "Удалить проблему",
    "Посмотреть список проблем",
    "Отмена",
    placeholder="Введите проблему",
    size=(2, 1, 1)
)

NAV_KB=get_keyboard(
    "Назад",
    "Отмена"
)