from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Assue

async def orm_add_assue(data: dict, session: AsyncSession):
    # Запись в бд
    obj = Assue(  # Создаем объект Assue для записи в БД
        name=data['name'],
        description=data['description'],
        decision=data['decision']
    )
    session.add(obj)
    await session.commit()  # Запись в БД

async def orm_get_assue(session: AsyncSession, assue_id: int):
    query = select(Assue).where(Assue.id == assue_id)
    result = await session.execute(query)
    print(result)
    return result.scalar()

async def orm_get_assues(session: AsyncSession):
    query = select(Assue)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_update_assue(data: dict, session: AsyncSession, assue_id: int):
    query = update(Assue).where(Assue.id == assue_id).values(
        name = data['name'],
        description = data['description'],
        decision = data['decision']
    )
    await session.execute(query)
    await session.commit()

async def orm_del_assue(session: AsyncSession, assue_id: int):
    obj = delete(Assue).where(Assue.id == assue_id)
    await session.execute(obj)
    await session.commit()