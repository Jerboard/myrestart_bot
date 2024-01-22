import sqlalchemy as sa
import typing as t

from datetime import datetime

from init import TZ
from db.base import METADATA, begin_connection


class PlotRow (t.Protocol):
    id: int
    created_at: datetime
    type: str
    comment: str
    file_id: str


PlotTable = sa.Table (
    'plots_cash',
    METADATA,
    sa.Column ('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column ('created_at', sa.DateTime),
    sa.Column ('type', sa.String (255)),
    sa.Column ('comment', sa.String (255)),
    sa.Column ('file_id', sa.String (255)),
  )


# добавить файл глобальный отчёт
async def add_plot_in_cache_global(type_: str, comment: str, file_id: str):
    now = datetime.now(TZ)
    async with begin_connection() as conn:
        await conn.execute(
            PlotTable.insert ().values (created_at=now, type=type_, comment=comment, file_id=file_id))


# добавить файл дневной отчет
async def add_plot_in_cache_daily(type_: str, user_id: int, file_id: str, new_entry: bool):
    now = datetime.now(TZ)
    payloads = dict(created_at=now, type=type_, comment=str(user_id), file_id=file_id)

    if new_entry:
        query = PlotTable.insert ().values (payloads)

    else:
        query = PlotTable.update ().values (payloads).where(PlotTable.c.comment == str(user_id))

    async with begin_connection() as conn:
        await conn.execute(query)


# возвращает файл
async def get_plot_cache(type_: str, comment: str) -> t.Union[PlotRow, None]:
    query = PlotTable.select().where(PlotTable.c.type == type_, PlotTable.c.comment == comment)

    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.first()
