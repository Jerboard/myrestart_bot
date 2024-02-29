from aiogram.types import Message, InputTextMessageContent, InlineQuery, InlineQueryResultArticle
from aiogram.fsm.context import FSMContext

import hashlib

import db
import keyboards as kb
from init import dp, bot, DATE_FORMAT, TIME_FORMAT
from handlers.user_settings import get_setting_main
from utils.text_utils import get_cut_text
from utils.data import cities_timezone


@dp.inline_query()
async def inline(call: InlineQuery, state: FSMContext):
    data = await state.get_data()
    print(data.get('on'))
    if data.get('on') == 'goals':
        results = await db.search_goals(
            user_id=call.from_user.id,
            search_query=call.query)

    elif data.get('on') == 'thanks':
        results = await db.search_thanks(
            user_id=call.from_user.id,
            search_query=call.query
        )

    elif data.get ('on') == 'timezone':
        results = []
        for tz_name, tz_info in cities_timezone.items():
            for city in tz_info['cities'].split(', '):
                if city.lower().startswith(call.query.lower()):
                    results.append({tz_name: tz_info})
                    break

        if not results:
            results = [{k: v} for k, v in cities_timezone.items()]

    else:
        results = ['error', ]

    search_results = []

    for result in results[:10]:
        if data.get ('on') == 'goals':
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

        elif data.get ('on') == 'timezone':
            # k = list(result.keys())[0]
            # print(k)
            k, v = list(result.items())[0]
            print(k, v)
            query_id = hashlib.md5 (k.encode ()).hexdigest ()
            title = v["name"]
            text = InputTextMessageContent (message_text=k)
            description = v['cities']

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
        if data ['on'] == 'goals':
            result_id = int (msg.text)
            result = await db.get_goal(result_id)
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
                reply_markup=kb.get_search_kb ('diary_goal_main')
            )

        elif data.get ('on') == 'thanks':
            result_id = int (msg.text)
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

        elif data.get ('on') == 'timezone':
            await db.update_user_info (user_id=msg.from_user.id, timezone=msg.text)
            await state.clear ()
            await get_setting_main (user_id=msg.from_user.id, message_id=data ['message_id'])
