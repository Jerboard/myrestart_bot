from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

import db
import keyboards as kb
from init import dp, bot, DATE_FORMAT
from utils.cover_photos import get_cover_photo
from enums import DiaryCB


# дневник благодарности старт
@dp.callback_query(lambda cb: cb.data.startswith(DiaryCB.DIARY_THANKS_MAIN.value))
async def diary_thanks_main(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    text = (f'<b>Дневник благодарности\n'
            f'Способствует освобождению от стресса и тревоги</b>\n\n'
            f'Регулярная практика благодарности стимулирует чувства вдохновения, надежды, силы и удовлетворенности '
            f'жизнью. Записи в Дневнике благодарности помогают освободиться от стресса и тревоги, обучая ценить '
            f'присутствующие в жизни моменты и людей.')
    photo = InputMediaPhoto (media=get_cover_photo('diary_thanks'), caption=text)
    await cb.message.edit_media (media=photo, reply_markup=kb.get_main_thanks_kb ())


# дневник благодарности написать
@dp.callback_query(lambda cb: cb.data.startswith(DiaryCB.DIARY_THANKS_SEND.value))
async def diary_thanks_main(cb: CallbackQuery, state: FSMContext):
    text = f'Напиши кого и за что ты хочешь поблагодарить'
    photo = InputMediaPhoto (media=get_cover_photo('diary_thanks'), caption=text)
    await state.set_state('send_thanks')
    await state.update_data(data={'message_id': cb.message.message_id})
    await cb.message.edit_media (media=photo, reply_markup=kb.get_back_button ('diary_thanks_main'))


# принимает благодарность
@dp.message(StateFilter('send_thanks'))
async def send_thanks(msg: Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    await state.clear()

    await db.add_thanks(msg.from_user.id, msg.text)
    text = '🙏 Благодарность принята'
    await bot.edit_message_caption(
        chat_id=msg.chat.id,
        message_id=data['message_id'],
        caption=text,
        reply_markup=kb.get_back_button('diary_thanks_main')
    )


# дневник благодарности архив сообщений
@dp.callback_query(lambda cb: cb.data.startswith(DiaryCB.ARCHIVE_THANKS.value))
async def goal_archive(cb: CallbackQuery, state: FSMContext):
    min_date = await db.get_thanks_min_date_user(cb.from_user.id)
    if not min_date:
        text = 'У вас нет ни одной записи в дневнике'
        await cb.answer(text, show_alert=True)
    else:
        await state.set_state('search')
        await state.update_data(data={
            'on': 'thanks',
            'message_id': cb.message.message_id
        })

        min_date_str = min_date.strftime(DATE_FORMAT)
        text = (f'Доступен поиск начиная с {min_date_str}\n\n'
                f'Введите число и месяц')
        photo = InputMediaPhoto (media=get_cover_photo('diary_thanks'), caption=text)
        await cb.message.edit_media (media=photo, reply_markup=kb.get_search_kb ('diary_thanks_main'))
