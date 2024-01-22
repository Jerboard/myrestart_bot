import sqlalchemy as sa
import typing as t

from datetime import date, datetime

from init import TZ
from db.base import METADATA, begin_connection


class UserRow(t.Protocol):
    id: int
    user_id: int
    full_name: str
    username: str
    email: str
    status: str
    end_date: date


UserTable = sa.Table(
    'users',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.Integer),
    sa.Column('full_name', sa.String(255)),
    sa.Column('username', sa.String(255)),
    sa.Column('email', sa.String(255)),
    sa.Column('status', sa.String(255)),
    sa.Column('end_date', sa.Date))


# возвращает информацию пользователя
async def get_user_info(user_id: int) -> t.Union[UserRow, None]:
    async with begin_connection() as conn:
        result = await conn.execute(
            UserTable.select().where(UserTable.c.user_id == user_id)
        )
    return result.first()


# сохраняет данные пользователя
async def add_user(user_id: int, full_name: str, username: str) -> None:
    today = datetime.now (TZ).date ()
    async with begin_connection() as conn:
        await conn.execute(
            UserTable.insert().values(
                user_id=user_id,
                full_name=full_name,
                username=username,
                status='new',
                end_date=today
            )
        )


# сохраняет данные пользователя
async def update_user_info(
        user_id: int,
        email: str = None,
        status: str = None,
        end_date: date = None) -> None:
    query = UserTable.update().where(UserTable.c.user_id == user_id)

    if email:
        query = query.values(email=email)
    if status:
        query = query.values(status=status)
    if end_date:
        query = query.values(end_date=end_date)

    async with begin_connection() as conn:
        await conn.execute(query)
