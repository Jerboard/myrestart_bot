import sqlalchemy as sa
import typing as t

from datetime import date, time, datetime

from init import TZ
from db.base import METADATA, begin_connection


class ThanksRow(t.Protocol):
    id: int
    user_id: int
    create_date: date
    create_time: time
    thank_1: str
    thank_2: str
    thank_3: str
    thank_4: str
    thank_5: str
    thank_6: str


ThanksTable = sa.Table(
    'thanks',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.Integer),
    sa.Column('create_date', sa.Date),
    sa.Column('create_time', sa.Time),
    sa.Column('thank_1', sa.Text),
    sa.Column('thank_2', sa.Text),
    sa.Column('thank_3', sa.Text),
    sa.Column('thank_4', sa.Text),
    sa.Column('thank_5', sa.Text),
    sa.Column('thank_6', sa.Text),
)


# добавляет строку состояния
async def add_thanks(
        user_id: int,
        thank_1: str,
        thank_2: str,
        thank_3: str,
        thank_4: str,
        thank_5: str,
        thank_6: str
) -> None:
    now = datetime.now(TZ)
    query = ThanksTable.insert().values(
        user_id=user_id,
        create_date=now.date(),
        create_time=now.time(),
        thank_1=thank_1,
        thank_2=thank_2,
        thank_3=thank_3,
        thank_4=thank_4,
        thank_5=thank_5,
        thank_6=thank_6
    )
    async with begin_connection () as conn:
        await conn.execute (query)


# возвращает все даты когда есть записи для пользователя
async def get_thanks_min_date_user(user_id: int) -> date:
    query = sa.select (sa.func.min (ThanksTable.c.create_date)).where (ThanksTable.c.user_id == user_id)
    async with begin_connection () as conn:
        result = await conn.scalar (query)
    return result


# поиск по благодарностям
async def search_thanks(user_id: int, search_query: str) -> tuple[ThanksRow]:
    query = ThanksTable.select().where(ThanksTable.c.user_id == user_id).limit(10)

    if search_query:
        date_str = search_query.replace ('/', '.').replace (' ', '.')
        date_split = date_str.split ('.')
        if len(date_split) == 0 and len(date_split[1]) > 0:
            day = int (date_split [0]) if date_split [0] != '' else None
            month = int(date_split[1]) if date_split[1] != '' else None
            query = query.where (
                sa.func.extract ('day', ThanksTable.c.create_date) == day,
                sa.func.extract ('month', ThanksTable.c.create_date) == month)

        else:
            query = query.where (ThanksTable.c.create_date.like(f'%{date_split [0]}%'))

    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.all()


# возвращает благодарность по id
async def get_thanks(thank_id: int) -> t.Union[ThanksRow, None]:
    async with begin_connection () as conn:
        result = await conn.execute (
            ThanksTable.select().where(ThanksTable.c.id == thank_id)
        )
    return result.first()
