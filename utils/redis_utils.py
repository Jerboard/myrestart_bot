from init import REDIS_CLIENT

import json

from datetime import timedelta


# сохраняет карточку
def save_card(user_id: int, card_id: str) -> None:
    REDIS_CLIENT.setex(
        name=f'current_card:{user_id}',
        time=timedelta (hours=6),
        value=card_id)


def get_current_card(user_id: int) -> str:
    return REDIS_CLIENT.get(f'current_card:{user_id}')


# сохраняет карточку
def save_stress_notify(data: dict) -> None:
    save_data = json.dumps (data)
    REDIS_CLIENT.set ('stress_notify_map', save_data)


def get_stress_notify() -> dict:
    data = REDIS_CLIENT.get ('stress_notify_map')
    return json.loads (data.decode ("utf-8"))