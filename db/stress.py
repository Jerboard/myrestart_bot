import sqlalchemy as sa
import typing as t
import random

from datetime import date, time, datetime, timedelta

from init import TZ
from db.base import METADATA, begin_connection


class StressRow(t.Protocol):
    id: int
    user_id: int
    create_date: date
    create_time: time
    is_good: bool


class GlobalStressData(t.Protocol):
    happy: int
    unhappy: int


class DailyStressData(t.Protocol):
    date: date
    day_rating: int


StressTable = sa.Table(
    'stress',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.Integer),
    sa.Column('create_date', sa.Date),
    sa.Column('create_time', sa.Time),
    sa.Column('is_good', sa.Boolean),
)


# добавляет строку состояния
async def add_stress_status(user_id: int, status: bool) -> None:
    now = datetime.now(TZ)
    query = StressTable.insert().values(
        user_id=user_id,
        create_date=now.date(),
        create_time=now.time(),
        is_good=status
    )
    async with begin_connection () as conn:
        await conn.execute (query)


# возвращает все даты когда есть записи для пользователя
async def get_stress_days_user(user_id: int):
    seven_days_ago = datetime.now(TZ) - timedelta(days=7)

    query = StressTable.select().where(StressTable.c.user_id == user_id,
                                       StressTable.c.create_date >= seven_days_ago.date())

    query_true = query.where(StressTable.c.is_good == True)
    query_false = query.where(StressTable.c.is_good == False)

    async with begin_connection () as conn:
        result_count_true = await conn.execute (query_true)
        result_count_false = await conn.execute (query_false)

    return {'happy': len(result_count_true.all()), 'unhappy': len(result_count_false.all())}


# время последнего заполнения
async def get_last_stress_time(user_id: int) -> t.Union[datetime, None]:
    query = StressTable.select().where(StressTable.c.user_id == user_id).order_by(sa.desc(StressTable.c.id))
    async with begin_connection () as conn:
        result = await conn.execute (query)
    last_row = result.first()
    if last_row:
        return datetime.combine(
            date=last_row.create_date,
            time=last_row.create_time)
    else:
        return None


# глобальный отчёт
async def get_global_stress_data(user_id: int) -> GlobalStressData:
    query = sa.select (
        sa.func.sum (sa.case ((StressTable.c.is_good == True, 1), else_=0)).label ('happy'),
        sa.func.sum (sa.case ((StressTable.c.is_good == False, 1), else_=0)).label ('unhappy'),
    ).where(StressTable.c.user_id == user_id)

    async with begin_connection () as conn:
        result = await conn.execute (query)

    return result.fetchone ()


# отчёт по дням
async def get_daily_stress_data(user_id: int) -> tuple[DailyStressData]:
    query = sa.select (
        StressTable.c.create_date,
        (sa.func.sum (sa.case ((StressTable.c.is_good == True, 1), else_=0)) -
         sa.func.sum (sa.case ((StressTable.c.is_good == False, 1), else_=0))).label ('day_rating')
    ).group_by (StressTable.c.create_date).where(StressTable.c.user_id == user_id)

    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.all()
