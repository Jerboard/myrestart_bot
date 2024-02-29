import sqlalchemy as sa
import typing as t

from datetime import date, time, datetime

from init import TZ
from db.base import METADATA, begin_connection


class GoalRow(t.Protocol):
    id: int
    user_id: int
    create_date: date
    create_time: time
    question_1: str
    question_2: str
    question_3: str
    question_4: str
    question_5: str


goalTable = sa.Table(
    'goals',
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
    query = sa.select (sa.func.min (goalTable.c.create_date)).where (goalTable.c.user_id == user_id)
    async with begin_connection () as conn:
        result = await conn.scalar (query)
    return result


# добавляет притяжение
async def add_goal(
        user_id: int,
        question_1: str,
        question_2: str,
        question_3: str,
        question_4: str = None,
        question_5: str = None
) -> None:
    now = datetime.now(TZ)
    async with begin_connection () as conn:
        await conn.execute(
            goalTable.insert().values(
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
async def search_goals(user_id: int, search_query: str) -> tuple[GoalRow]:
    query = goalTable.select().where(goalTable.c.user_id == user_id).limit(10)

    if search_query:
        date_str = search_query.replace ('/', '.').replace (' ', '.')
        date_split = date_str.split ('.')
        day = int (date_split [0]) if date_split [0] != '' else None
        if len(date_split) == 0 and len(date_split[1]) > 0:
            month = int(date_split[1]) if date_split[1] != '' else None
            query = query.where (
                sa.func.extract ('day', goalTable.c.create_date) == day,
                sa.func.extract ('month', goalTable.c.create_date) == month)

        else:
            query = query.where (goalTable.c.create_date.like(f'%{date_split [0]}%'))

    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.all()


# возвращает притяжение по id
async def get_goal(goal_id: int) -> t.Union[GoalRow, None]:
    async with begin_connection () as conn:
        result = await conn.execute (
            goalTable.select().where(goalTable.c.id == goal_id)
        )
    return result.first()
