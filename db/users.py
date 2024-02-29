import sqlalchemy as sa
import typing as t

from datetime import date, datetime

from init import TZ
from db.base import METADATA, begin_connection
from enums import UserStatus


class UserRow(t.Protocol):
    id: int
    user_id: int
    full_name: str
    username: str
    email: str
    status: str
    end_date: date
    notify_goal: bool
    notify_stress: bool
    notify_thank: bool
    notify_card: bool
    timezone: str
    start_trial: datetime


UserTable = sa.Table(
    'users',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.Integer),
    sa.Column('full_name', sa.String(255)),
    sa.Column('username', sa.String(255)),
    sa.Column('email', sa.String(255)),
    sa.Column('status', sa.String(255)),
    sa.Column('end_date', sa.Date),
    sa.Column('notify_goal', sa.Boolean, default=False),
    sa.Column('notify_stress', sa.Boolean, default=False),
    sa.Column('notify_thank', sa.Boolean, default=False),
    sa.Column('notify_card', sa.Boolean, default=False),
    sa.Column('timezone', sa.String(255), default='Europe/Moscow'),
    sa.Column('start_trial', sa.DateTime(timezone=True)),
)


# возвращает информацию пользователя
async def get_user_info(user_id: int) -> t.Union[UserRow, None]:
    async with begin_connection() as conn:
        result = await conn.execute(
            UserTable.select().where(UserTable.c.user_id == user_id)
        )
    return result.first()


# возвращает информацию пользователя
async def get_users_notify() -> tuple[UserRow]:
    async with begin_connection() as conn:
        result = await conn.execute(
            UserTable.select().where(UserTable.c.status == UserStatus.ACTIVE.value)
        )
    return result.all()


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
        end_date: date = None,
        notify_goal: bool = None,
        notify_stress: bool = None,
        notify_thank: bool = None,
        notify_card: bool = None,
        timezone: str = None,
        start_trial: t.Union[datetime, str] = None
) -> None:
    query = UserTable.update().where(UserTable.c.user_id == user_id)

    if email:
        query = query.values(email=email)
    if status:
        query = query.values(status=status)
    if end_date:
        query = query.values(end_date=end_date)
    if timezone:
        query = query.values(timezone=timezone)
    if start_trial:
        if start_trial == 'stop':
            start_trial = None
        query = query.values(start_trial=start_trial)

    if notify_goal is not None:
        query = query.values (notify_goal=notify_goal)
    if notify_stress is not None:
        query = query.values (notify_stress=notify_stress)
    if notify_thank is not None:
        query = query.values (notify_thank=notify_thank)
    if notify_card is not None:
        query = query.values (notify_card=notify_card)

    async with begin_connection() as conn:
        await conn.execute(query)
