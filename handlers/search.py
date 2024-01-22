from aiogram.types import Message, InputTextMessageContent, InlineQuery, InlineQueryResultArticle
from aiogram.fsm.context import FSMContext

import hashlib

import db
import keyboards as kb
from init import dp, bot, DATE_FORMAT, TIME_FORMAT
from utils.text_utils import get_cut_text


@dp.inline_query()
async def inline(call: InlineQuery, state: FSMContext):
    data = await state.get_data()
    if data.get('on') == 'attractions':
        results = await db.search_attractions(
            user_id=call.from_user.id,
            search_query=call.query)

    elif data.get('on') == 'thanks':
        results = await db.search_thanks(
            user_id=call.from_user.id,
            search_query=call.query
        )

    else:
        results = ['error', ]

    search_results = []

    for result in results:
        if data.get ('on') == 'attractions':
            description = (f'1: {get_cut_text(50, result.question_1)}\n'
                           f'2: {get_cut_text(50, result.question_2)}\n'
                           f'3: {get_cut_text(50, result.question_3)}\n'
                           f'4: {get_cut_text(50, result.question_4)}\n'
                           f'5: {get_cut_text(50, result.question_5)}')

            query_id = hashlib.md5(f'{result.id}'.encode()).hexdigest()
            date_str = result.create_date.strftime (DATE_FORMAT)
            time_str = result.create_time.strftime (TIME_FORMAT)
            title = f'{date_str} {time_str}'
            text = InputTextMessageContent(message_text=f'{result.id}')

        elif data.get ('on') == 'thanks':
            description = get_cut_text(50, result.text)
            query_id = hashlib.md5 (f'{result.id}'.encode ()).hexdigest ()

            date_str = result.create_date.strftime (DATE_FORMAT)
            time_str = result.create_time.strftime (TIME_FORMAT)
            title = f'{date_str} {time_str}'
            text = InputTextMessageContent (message_text=f'{result.id}')

        else:
            query_id = hashlib.md5 (f'1'.encode ()).hexdigest ()
            title = 'Параметры поиска не найдены'
            text = InputTextMessageContent (message_text=f'/start')
            description = 'Выберите журнал, и нажмите "🔍 Поиск"'

        item = InlineQueryResultArticle(
            id=query_id,
            title=title,
            input_message_content=text,
            description=description
        )
        search_results.append(item)

    await call.answer(search_results, cache_time=60, is_personal=True)


# результат
@dp.message(lambda msg: msg.via_bot is not None)
async def get_video(msg: Message, state: FSMContext):
    data = await state.get_data ()
    if not data:
        pass
    else:
        await msg.delete()
        result_id = int(msg.text)
        if data ['on'] == 'attractions':
            result = await db.get_attraction(result_id)
            date_str = result.create_date.strftime (DATE_FORMAT)
            time_str = result.create_time.strftime (TIME_FORMAT)
            text = (
                f'Притяжение от {date_str} {time_str}:\n\n'
                f'1: {result.question_1}\n'
                f'2: {result.question_2}\n'
                f'3: {result.question_3}\n'
                f'4: {result.question_4}\n'
                f'5: {result.question_5}')

            await bot.edit_message_caption(
                chat_id=msg.chat.id,
                message_id=data['message_id'],
                caption=text,
                reply_markup=kb.get_search_kb ('diary_attraction_main')
            )

        elif data.get ('on') == 'thanks':
            result = await db.get_thanks(result_id)
            date_str = result.create_date.strftime(DATE_FORMAT)
            time_str = result.create_time.strftime(TIME_FORMAT)
            text = (f'Благодарность от {date_str} {time_str}:\n\n'
                    f'{result.text}')

            await bot.edit_message_caption (
                chat_id=msg.chat.id,
                message_id=data ['message_id'],
                caption=text,
                reply_markup=kb.get_search_kb ('diary_thanks_main')
            )
