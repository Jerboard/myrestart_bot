from aiogram.types import CallbackQuery, InputMediaPhoto

import db
import keyboards as kb
from init import dp
from utils.cover_photos import get_cover_photo


# ЛК основное меню
@dp.callback_query(lambda cb: cb.data.startswith('account_start'))
async def account_start(cb: CallbackQuery):
    user_info = await db.get_user_info (cb.from_user.id)
    if user_info.status != 'active':
        text = 'Для доступа в личный кабинет оплатите подписку'
        photo = InputMediaPhoto (media=get_cover_photo ('profile'), caption=text)
        await cb.message.edit_media (media=photo, reply_markup=kb.get_account_not_active_kb ())

    else:
        text = 'Здесь сообщение поясняющее'
        photo = InputMediaPhoto (media=get_cover_photo('profile'), caption=text)
        await cb.message.edit_media (media=photo, reply_markup=kb.get_main_account_kb ())
