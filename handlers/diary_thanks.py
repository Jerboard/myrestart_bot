from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

import db
import keyboards as kb
from init import dp, bot, DATE_FORMAT
from utils.cover_photos import get_cover_photo
from utils.data import thanks_questions_text
from enums import DiaryCB, DiaryState


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
    text = thanks_questions_text [1]
    await state.set_state(DiaryState.SEND_THANKS)
    await state.update_data(data={
        'message_id': cb.message.message_id,
        'step': 1,
        'text': text
    })
    photo = InputMediaPhoto (media=get_cover_photo('diary_thanks'), caption=text)
    await cb.message.edit_media (media=photo, reply_markup=kb.get_back_button ('diary_thanks_main'))


# принимает благодарность
@dp.message(StateFilter(DiaryState.SEND_THANKS))
async def send_thanks(msg: Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    print(data)

    if data['step'] < 3:
        # bottom_text = thanks_questions_text[1]
        bottom_text = ''
    elif data['step'] == 3:
        bottom_text = thanks_questions_text[2]
    elif data['step'] == 4:
        bottom_text = thanks_questions_text[3]
    elif data['step'] == 5:
        bottom_text = thanks_questions_text[4]
    else:
        await state.clear()
        await db.add_thanks(
            user_id=msg.from_user.id,
            thank_1=data['thank_1'],
            thank_2=data['thank_2'],
            thank_3=data['thank_3'],
            thank_4=data['thank_4'],
            thank_5=data['thank_5'],
            thank_6=msg.text,
        )
        bottom_text = '\n🙏 Благодарность принята'

    text = (f'{data["text"]}\n'
            f'<i>{msg.text}</i>\n'
            f'{bottom_text}').strip()

    if data['step'] < 6:
        await state.update_data (data={
            'text': text,
            'step': data['step'] + 1,
            f'thank_{data["step"]}': msg.text
        })

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


'''
Записать 📝 благодарности в дневник?
Да / Нет

Благодарность себе / миру

Благодарность себе 
За что я благодарю себя сегодня?
 1. Ответ
 2. Ответ
 3. Ответ

Благодарность - 1/3
За что я благодарен этому дню?
Ответ
Благодарность - 2/3
Кому я благодарен из моего окружения?
Ответ
Благодарность - 3/3
За что бы хотелось поблагодарить в будущем?
Ответ
'''
