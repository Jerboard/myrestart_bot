from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile

from datetime import datetime, timedelta
import os

import db
import keyboards as kb
from init import dp, TZ
from utils.cover_photos import get_cover_photo
from utils.plots import get_global_stress_plot, get_daily_stress_plot


# ЛК основное меню
@dp.callback_query(lambda cb: cb.data.startswith('diary_stress_main'))
async def account_start(cb: CallbackQuery):
    count_stress = await db.get_stress_days_user(cb.from_user.id)
    text = (f'За последние 7 дней выбыли напряжены {count_stress["unhappy"]} раз и '
            f'расслаблены {count_stress["happy"]} раз')
    photo = InputMediaPhoto (media=get_cover_photo('diary_stress'), caption=text)
    await cb.message.edit_media (media=photo, reply_markup=kb.get_main_stress_kb ())


# отметить состояние
@dp.callback_query(lambda cb: cb.data.startswith('diary_stress_check_choice'))
async def account_start(cb: CallbackQuery):
    last_add = await db.get_last_stress_time(cb.from_user.id)

    if last_add:
        last_add_tz = TZ.localize(last_add)
        hour_ago = datetime.now(TZ) - timedelta(hours=1)

        if last_add_tz > hour_ago:
            timer = last_add_tz - hour_ago
            timer_minutes = timer.seconds // 60
            await cb.answer(f'Час ещё не прошёл осталось {timer_minutes} мин.', show_alert=True)
            return

    text = 'Выберете своё состояние расслабленное/напряжённое'
    photo = InputMediaPhoto (media=get_cover_photo('diary_stress'), caption=text)
    await cb.message.edit_media (media=photo, reply_markup=kb.get_check_stress_kb ())


# отметить состояние
@dp.callback_query(lambda cb: cb.data.startswith('diary_stress_check_add'))
async def account_start(cb: CallbackQuery):
    _, is_good_str = cb.data.split(':')
    await db.add_stress_status(user_id=cb.from_user.id, status=bool(int(is_good_str)))
    await cb.answer('Состояние зафиксировано')

    text = 'Здесь сообщение поясняющее'
    photo = InputMediaPhoto (media=get_cover_photo('diary_stress'), caption=text)
    await cb.message.edit_media (media=photo, reply_markup=kb.get_main_account_kb ())


# архив состояний состояние
@dp.callback_query(lambda cb: cb.data.startswith('diary_stress_archive'))
async def account_start(cb: CallbackQuery):
    _, plot_type = cb.data.split (':')

    if plot_type == 'global':
        global_plot_data = await db.get_global_stress_data(cb.from_user.id)
        if global_plot_data.happy == 0 and global_plot_data.unhappy == 0:
            await cb.answer('У вас нет ни одной записи в дневнике')
            return

        else:
            bit = 1200 / (global_plot_data.happy + global_plot_data.unhappy)
            happy_count = round(global_plot_data.happy * bit)
            unhappy_count = round(global_plot_data.unhappy * bit)
            plot_ident = f'{happy_count}:{happy_count}'

            text = 'График состояния за весь период'

            cached_plot = await db.get_plot_cache(type_=plot_type, comment=plot_ident)
            if cached_plot:
                photo = InputMediaPhoto (media=cached_plot.file_id, caption=text)
                await cb.message.edit_media (media=photo, reply_markup=kb.get_archive_stress_kb (plot_type))

            else:
                get_global_stress_plot(
                    user_id=cb.from_user.id,
                    happy=happy_count,
                    unhappy=unhappy_count
                )
                photo_path = os.path.join ('temp', f'{plot_type}_{cb.from_user.id}.jpg')
                photo_input = FSInputFile (photo_path)

                photo = InputMediaPhoto (media=photo_input, caption=text)
                sent = await cb.message.edit_media (media=photo, reply_markup=kb.get_archive_stress_kb (plot_type))
                await db.add_plot_in_cache_global(type_=plot_type, comment=plot_ident, file_id=sent.photo[-1].file_id)

                os.remove(photo_path)

    else:
        text = 'График состояния по дням'

        last_stress_add = await db.get_last_stress_time(cb.from_user.id)
        cached_plot = await db.get_plot_cache(type_=plot_type, comment=str(cb.from_user.id))

        if cached_plot and cached_plot.created_at > last_stress_add:
            photo = InputMediaPhoto (media=cached_plot.file_id, caption=text)
            await cb.message.edit_media (media=photo, reply_markup=kb.get_archive_stress_kb (plot_type))

        else:
            daily_plot_data = await db.get_daily_stress_data(user_id=cb.from_user.id)
            get_daily_stress_plot(user_id=cb.from_user.id, data=daily_plot_data)

            photo_path = os.path.join ('temp', f'{plot_type}_{cb.from_user.id}.jpg')
            photo_input = FSInputFile (photo_path)

            photo = InputMediaPhoto (media=photo_input, caption=text)
            sent = await cb.message.edit_media (media=photo, reply_markup=kb.get_archive_stress_kb (plot_type))

            await db.add_plot_in_cache_daily (
                type_=plot_type,
                user_id=cb.from_user.id,
                file_id=sent.photo [-1].file_id,
                new_entry=True if cached_plot is None else False
            )

            os.remove (photo_path)
