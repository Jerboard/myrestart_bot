from init import REDIS_CLIENT

from datetime import timedelta


# сохраняет карточку
def save_card(user_id: int, card_id: str) -> None:
    REDIS_CLIENT.setex(
        name=f'current_card:{user_id}',
        time=timedelta (hours=6),
        value=card_id)


def get_current_card(user_id: int) -> str:
    return REDIS_CLIENT.get(f'current_card:{user_id}')
