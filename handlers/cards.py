from aiogram.types import CallbackQuery, InputMediaPhoto

import db
from init import dp
import keyboards as kb
from utils import redis_utils as redis
from utils.cover_photos import get_cover_photo


# Карты старт
@dp.callback_query(lambda cb: cb.data.startswith('cards_main'))
async def diary_thanks_main(cb: CallbackQuery):
    text = 'Это ваше меню'
    photo = InputMediaPhoto (media=get_cover_photo ('choice_card'), caption=text)
    await cb.message.edit_media (media=photo, reply_markup=kb.get_main_card_kb ())


# выдаёт карту
@dp.callback_query(lambda cb: cb.data.startswith('get_card'))
async def diary_thanks_main(cb: CallbackQuery):
    current_card = redis.get_current_card(cb.from_user.id)
    if not current_card:
        current_card = await db.get_random_card_id()
        redis.save_card(cb.from_user.id, current_card)

    text = 'Задавай этот вопрос себе несколько раз в день'
    photo = InputMediaPhoto (media=current_card, caption=text)
    await cb.message.edit_media (media=photo, reply_markup=kb.get_back_button ('cards_main'))
