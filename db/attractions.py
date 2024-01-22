import sqlalchemy as sa
import typing as t

from datetime import date, time, datetime

from init import TZ
from db.base import METADATA, begin_connection


class AttractionRow(t.Protocol):
    id: int
    user_id: int
    create_date: date
    create_time: time
    question_1: str
    question_2: str
    question_3: str
    question_4: str
    question_5: str


AttractionTable = sa.Table(
    'attractions',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.Integer),
    sa.Column('create_date', sa.Date),
    sa.Column('create_time', sa.Time),
    sa.Column('question_1', sa.Text),
    sa.Column('question_2', sa.Text),
    sa.Column('question_3', sa.Text),
    sa.Column('question_4', sa.Text),
    sa.Column('question_5', sa.Text),
)


# возвращает все даты когда есть записи для пользователя
async def get_all_attr_date_user(user_id: int) -> date:
    query = sa.select (sa.func.min (AttractionTable.c.create_date)).where (AttractionTable.c.user_id == user_id)
    async with begin_connection () as conn:
        result = await conn.scalar (query)
    return result


# добавляет притяжение
async def add_attraction(
        user_id: int,
        question_1: str,
        question_2: str,
        question_3: str,
        question_4: str,
        question_5: str
) -> None:
    now = datetime.now(TZ)
    async with begin_connection () as conn:
        await conn.execute(
            AttractionTable.insert().values(
                user_id=user_id,
                create_date=now.date(),
                create_time=now.time(),
                question_1=question_1,
                question_2=question_2,
                question_3=question_3,
                question_4=question_4,
                question_5=question_5
            ))


# поиск по притяжениям
async def search_attractions(user_id: int, search_query: str) -> tuple[AttractionRow]:
    query = AttractionTable.select().where(AttractionTable.c.user_id == user_id).limit(10)

    if search_query:
        date_str = search_query.replace ('/', '.').replace (' ', '.')
        date_split = date_str.split ('.')
        day = int (date_split [0]) if date_split [0] != '' else None
        # month = int (date_split [1]) if date_split [1] != '' else None
        if len(date_split) == 0 and len(date_split[1]) > 0:
            # day = int(date_split[0]) if date_split[0] != '' else None
            month = int(date_split[1]) if date_split[1] != '' else None
            query = query.where (
                sa.func.extract ('day', AttractionTable.c.create_date) == day,
                sa.func.extract ('month', AttractionTable.c.create_date) == month)

        else:
            query = query.where (AttractionTable.c.create_date.like(f'%{date_split [0]}%'))

    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.all()


# возвращает притяжение по id
async def get_attraction(attraction_id: int) -> t.Union[AttractionRow, None]:
    async with begin_connection () as conn:
        result = await conn.execute (
            AttractionTable.select().where(AttractionTable.c.id == attraction_id)
        )
    return result.first()
