from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

import db
import keyboards as kb
from init import dp, bot, DATE_FORMAT
from utils.cover_photos import get_cover_photo


# дневник притяжений основное меню
@dp.callback_query(lambda cb: cb.data.startswith('diary_attraction_main'))
async def diary_attraction(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    text = 'Дневник притяжений'
    photo = InputMediaPhoto (media=get_cover_photo('diary_attraction'), caption=text)
    await cb.message.edit_media (media=photo, reply_markup=kb.get_main_attraction_kb ())


# дневник притяжений архив сообщений
@dp.callback_query(lambda cb: cb.data.startswith('archive_attraction'))
async def attraction_archive(cb: CallbackQuery, state: FSMContext):
    min_date = await db.get_all_attr_date_user(cb.from_user.id)
    if not min_date:
        text = 'У вас нет ни одной записи в дневнике'
        await cb.answer(text, show_alert=True)
    else:
        await state.set_state('search')
        await state.update_data(data={
            'on': 'attractions',
            'message_id': cb.message.message_id
        })

        min_date_str = min_date.strftime(DATE_FORMAT)
        text = (f'Доступен поиск начиная с {min_date_str}\n\n'
                f'Введите число и месяц')
        photo = InputMediaPhoto (media=get_cover_photo('diary_attraction'), caption=text)
        await cb.message.edit_media (media=photo, reply_markup=kb.get_search_kb ('diary_attraction_main'))
        # await cb.message.edit_media (media=photo, reply_markup=kb.get_back_button ('diary_attraction_main'))


# дневник притяжений опрос
@dp.callback_query(lambda cb: cb.data.startswith('add_attraction'))
async def add_attraction(cb: CallbackQuery, state: FSMContext):
    text = f'Какие цели и изменения вы хотели бы добавить в свою жизнь?\n\nВопрос 1'
    await state.set_state('add_attraction')
    await state.update_data(data={
        'question': 1,
        'message_id': cb.message.message_id,
        'text': text
    })

    photo = InputMediaPhoto (media=get_cover_photo ('diary_attraction'), caption=text)
    await cb.message.edit_media (media=photo, reply_markup=kb.get_back_button ('diary_attraction_main'))


# принимает ответы
@dp.message(StateFilter('add_attraction'))
async def add_attraction_answers(msg: Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    question = data["question"]
    main_text = data['text'].split('\n\n')[0]

    if question == 1:
        bottom_text = f'Вопрос 2'
    elif question == 2:
        bottom_text = f'Вопрос 3'
    elif question == 3:
        bottom_text = f'Вопрос 4'
    elif question == 4:
        bottom_text = f'Вопрос 5'
    else:
        await db.add_attraction (
            user_id=msg.from_user.id,
            question_1=data ['answer_1'],
            question_2=data ['answer_2'],
            question_3=data ['answer_3'],
            question_4=data ['answer_4'],
            question_5=msg.text
        )
        await state.clear ()

        bottom_text = 'Добавлено в дневник'

    text = (f'{main_text}\n'
            f'{question}: {msg.text}\n\n'
            f'{bottom_text}')

    if question < 5:
        await state.update_data(data={
            'question': question + 1,
            f'answer_{question}': msg.text,
            'text': text
        })

    await bot.edit_message_caption(
        chat_id=msg.chat.id,
        message_id=data['message_id'],
        caption=text,
        reply_markup=kb.get_back_button ('diary_attraction_main')
    )
