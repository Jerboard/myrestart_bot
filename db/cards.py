import sqlalchemy as sa
import typing as t

from db.base import METADATA, begin_connection


class CardRow (t.Protocol):
    id: int
    file_id: str


CardTable = sa.Table (
    'cards',
    METADATA,
    sa.Column ('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column ('file_id', sa.String (255)),
  )


# Сохраняет карту
async def add_card(file_id: str) -> None:
    async with begin_connection () as conn:
        await conn.execute (
            CardTable.insert().values(file_id=file_id)
        )


# Возвращает случайную карту
async def get_random_card_id() -> str:
    async with begin_connection () as conn:
        result = await conn.execute (
            CardTable.select().with_only_columns(CardTable.c.file_id).order_by(sa.func.random()).limit(1)
        )
    return result.first()[0]
