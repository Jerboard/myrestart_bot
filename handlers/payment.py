from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.enums.message_entity_type import MessageEntityType

from asyncio import sleep
from datetime import datetime, timedelta

import db
import keyboards as kb
from init import dp, bot, DATE_FORMAT, TZ
from utils.cover_photos import get_cover_photo
from utils.data import tariffs


# дневник притяжений основное меню
@dp.callback_query(lambda cb: cb.data.startswith('start_payment'))
async def start_payment(cb: CallbackQuery, state: FSMContext):
    user_info = await db.get_user_info (cb.from_user.id)

    if user_info.email:
        text = 'Выберите тариф:'
        photo = InputMediaPhoto (media=get_cover_photo ('payment'), caption=text)
        await cb.message.edit_media (
            media=photo,
            reply_markup=kb.get_tariff_kb ())

    else:
        text = 'Отправьте адрес электронной почты'

        await state.set_state('send_email')
        await state.update_data(data={'message_id': cb.message.message_id})
        photo = InputMediaPhoto (media=get_cover_photo ('payment'), caption=text)
        await cb.message.edit_media (media=photo, reply_markup=kb.get_back_button ('back_start'))


# принимает адрес почты
@dp.message(StateFilter('send_email'))
async def send_email(msg: Message, state: FSMContext):
    await msg.delete()
    entity = msg.entities[0] if msg.entities else None
    if not entity or entity.type != MessageEntityType.EMAIL:
        text = (f'<code>{msg.text}</code> не является адресом электронной почты\n\n'
                f'Пожалуйста отправьте почту сообщением')
        sent = await msg.answer(text)
        await sleep(5)
        await sent.delete()

    else:
        data = await state.get_data()
        await state.clear()
        await db.update_user_info(user_id=msg.from_user.id,  email=msg.text)

        text = 'Выберите тариф:'
        photo = InputMediaPhoto (media=get_cover_photo ('payment'), caption=text)
        await bot.edit_message_media (
            chat_id=msg.chat.id,
            message_id=data['message_id'],
            media=photo,
            reply_markup=kb.get_tariff_kb ())


# ссылка на страницу оплаты и кнопка подтверждения
@dp.callback_query(lambda cb: cb.data.startswith('payment_tariff'))
async def payment_tariff(cb: CallbackQuery):
    _, tariff_id = cb.data.split(':')

    tariff = tariffs[tariff_id]
    user_info = await db.get_user_info(cb.from_user.id)
    today = datetime.now(TZ).date()

    end_date = today if user_info.end_date <= today else user_info.end_date

    for i in range(0, tariff['duration']):
        end_date = end_date + timedelta(days=30)

    await db.update_user_info(user_id=cb.from_user.id, end_date=end_date, status='active')
    text = (f'Оплата прошла успешно\n\n'
            f'Ваша подписка истекает: {end_date.strftime(DATE_FORMAT)}')

    photo = InputMediaPhoto (media=get_cover_photo ('pay_conf'), caption=text)
    await cb.message.edit_media (media=photo, reply_markup=kb.get_end_payment_kb ())
