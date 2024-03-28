from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession


from ..filters.chat_types import ChatTypeFilter, IsAdmin
from ..keyboards.kbd import ADMIN_KB
from ..database.orm_query import orm_add_assue, orm_get_assues

print('Проверка')
admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin())
print('Проверка прошла')


@admin_router.message(Command("admin"))
async def add_issue(message: types.Message):
    await message.answer("Выберите действие", reply_markup=ADMIN_KB)

@admin_router.message(F.text.lower() == 'посмотреть список проблем')
async def get_assue_list(message: types.Message, session: AsyncSession):
    assue_list = await orm_get_assues(session=session)
    for assue in assue_list:
        await message.answer(f"{assue.name}")

# Код для машины состояний. Состояния машины состояний
class AddAssue(StatesGroup):
    name = State()
    description = State()
    decision = State()

    texts = {
        'AddAssue:name': 'Введите заново название',  # Такие 'AddAssue:name' строки возвращает state.get_state()
        'AddAssue:description': 'Введите заново описание',
        'AddAssue:decision': 'Введите заново решение',
    }


# Хэндлеры машины состояния
@admin_router.message(StateFilter(None),
                      F.text == "Добавить проблему")  # StateFilter(None) - проверка состояния пользователя
async def add_faq(message: types.Message, state: FSMContext):  # state  - состояние пользователя обязательно пробросить
    await message.answer("Введите название проблемы", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddAssue.name)  # Встаем в состояние ожидания ввода названия


@admin_router.message(StateFilter('*'), Command('отмена'))  # State.Filter('*') - любое состояние машины
@admin_router.message(StateFilter('*'), F.text.casefold() == 'отмена')  # casefold - переводит в нижний регистр
async def cansel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.answer('Действия отменены', reply_markup=ADMIN_KB)
    await state.clear()


@admin_router.message(StateFilter('*'), Command('назад'))  # State.Filter('*') - любое состояние машины
@admin_router.message(StateFilter('*'), F.text.casefold() == 'назад')  # casefold - переводит в нижний регистр
async def cansel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == AddAssue.name:
        await message.answer('Предыдущего действия нет. Напишите \"отмена\" или введите название проблемы')
        return
    previos = None
    for step in AddAssue.__all_states__:
        if step.state == current_state:
            await state.set_state(previos)
            await message.answer(f'Вы вернулись к прошлому шагу \n {AddAssue.texts[previos.state]}')
            return
        previos = step
    await message.answer('Шага нет', reply_markup=ADMIN_KB)


@admin_router.message(AddAssue.name, F.text)
async def add_faq_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)  # Сохрание введенных данных в словарь в хранилище
    await message.answer("Введите описание проблемы")
    await state.set_state(AddAssue.description)


# Если пользователь вводит какую то ересь
@admin_router.message(AddAssue.name, F.content_type.in_({'emoji', 'photo'}) )
async def bad_name(message: types.Message, state: FSMContext):
    await message.answer("Неккоректные данные, ебланько. Введите название проблемы")


@admin_router.message(AddAssue.description,
                      F.text)  # AddAssue.name - проверка что машина в состоянии ожидания ввода name
async def add_faq_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите решение проблемы")
    await state.set_state(AddAssue.decision)


# Если пользователь вводит какую то ересь
@admin_router.message(AddAssue.description)
async def bad_description(message: types.Message, state: FSMContext):
    await message.answer("Неккоректные данные, ебланько. Введите описание проблемы",)


@admin_router.message(AddAssue.decision, F.text)
async def add_faq(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(decision=message.text)

    data = await state.get_data()  # Данные в виде словаря (json)

    #Запись в бд
    try:
        await orm_add_assue(data=data, session=session)
        await message.answer("Данные успешно записаны", reply_markup=ADMIN_KB)
    except Exception as e:
        await message.answer(f"Произошла ошибка. Вот её текст: \n {str(e)}", reply_markup=ADMIN_KB)
    await message.answer(str(data))
    await state.clear()



# Конец машины состояния
