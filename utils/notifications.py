from pytz import timezone
from datetime import datetime, timedelta

import random

import db
import keyboards as kb
from init import bot, scheduler, TZ, log_error, DATETIME_FORMAT
from utils.cover_photos import get_cover_photo
from utils import redis_utils as redis
from enums import UserStatus


async def notifications_scheduler():
    scheduler.add_job (send_notify, 'cron', minute=0)
    scheduler.add_job (create_notify_stress_map, 'cron', hour=0, minute=0)
    scheduler.add_job (send_notify_stress, 'cron', second=0)
    scheduler.start ()


# отправляет напоминания
async def send_notify():
    users = await db.get_users_notify()
    now = datetime.now(TZ)

    for user_info in users:
        user_timezone = timezone(user_info.timezone)
        user_time = datetime.now(user_timezone)

        text = None
        notify_type = None

        if user_info.notify_goal and user_time.hour == 8:

            text = 'Напоминание дневник целей'
            notify_type = 'goal'

        # elif user_info.notify_stress and (12 <= user_time.hour <= 19):
        #     text = 'Напоминание дневник состояния'
        #     notify_type = 'stress'

        elif user_info.notify_thank and user_time.hour == 21:
            text = 'Напоминание дневник благодарности'
            notify_type = 'thank'

        elif user_info.notify_card and user_time.hour == 11:
            text = 'Напоминание выберите карту'
            notify_type = 'card'

        if text and notify_type:
            await bot.send_photo(
                chat_id=user_info.user_id,
                photo=get_cover_photo('notice'),
                caption=text,
                protect_content=True,
                reply_markup=kb.get_notify_kb(notify_type)
            )

        if user_info.start_trial:
            end_trial_time = user_info.start_trial + timedelta(hours=54)
            if TZ.localize(end_trial_time) < now:
                await db.update_user_info(
                    user_id=user_info.user_id,
                    status=UserStatus.INACTIVE.value,
                    start_trial='stop'
                )


# составляет карту напоминаний журнала стресса
async def create_notify_stress_map():
    users = await db.get_users_notify(only_stress=True)

    notify_map = {}
    for user_info in users:
        random_hour = random.randint (11, 19)
        random_minute = random.randint (0, 59)

        user_timezone = timezone (user_info.timezone)
        user_time = datetime.now (user_timezone).replace (hour=random_hour, minute=random_minute, second=0, microsecond=0)
        msc_time = user_time.astimezone (TZ)

        notify_map[user_info.user_id] = {
            'user_time': user_time.strftime(DATETIME_FORMAT),
            'msc_time': msc_time.strftime(DATETIME_FORMAT)
        }

    redis.save_stress_notify(notify_map)
    log_error(f'Карта напоминаний дневник состояния:\n{notify_map}')


# отправляет напоминание дневник состояния
async def send_notify_stress():
    notify_map = redis.get_stress_notify()

    now = datetime.now(TZ).replace(second=0, microsecond=0)
    log_error(f'Запуск напоминания стресс {now}')
    for k, v in notify_map.items():
        user_notify_time = datetime.strptime(v['msc_time'], DATETIME_FORMAT)

        if user_notify_time == now:
            user_info = await db.get_user_info(k)
            if user_info.notify_stress:
                await bot.send_photo (
                    chat_id=user_info.user_id,
                    photo=get_cover_photo ('notice'),
                    caption='Напоминание дневник состояния',
                    protect_content=True,
                    reply_markup=kb.get_notify_kb ('stress')
                )

                log_error(f'Дневник состояния напоминание отправлено.\n'
                          f'Пользователь: {user_info.full_name}\n'
                          f'Время: {v["user_time"]}\n'
                          f'Московское время: {v["msc_time"]}\n')


'''
Напоминание
- Цели 8 утра
- Состояние
рандомно с 12 до 19
- благодарность 21
- карты в 11:00 , выбрать карту
'''
