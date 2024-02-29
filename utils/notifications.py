from pytz import timezone
from datetime import datetime, timedelta

import db
import keyboards as kb
from init import bot, scheduler, TZ
from enums import UserStatus


async def notifications_scheduler():
    scheduler.add_job (send_notify, 'cron', minute=0)
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

        elif user_info.notify_stress and (12 <= user_time.hour <= 19):
            text = 'Напоминание дневник состояния'
            notify_type = 'stress'

        elif user_info.notify_thank and user_time.hour == 21:
            text = 'Напоминание дневник благодарности'
            notify_type = 'thank'

        elif user_info.notify_card and user_time.hour == 11:
            text = 'Напоминание выберите карту'
            notify_type = 'card'

        if text and notify_type:
            await bot.send_message(
                chat_id=user_info.user_id,
                text=text,
                protect_content=True,
                reply_markup=kb.get_notify_kb(notify_type)
            )

        if user_info.start_trial:
            end_trial_time = user_info.start_trial + timedelta(hours=54)
            if end_trial_time < now:
                await db.update_user_info(
                    user_id=user_info.user_id,
                    status=UserStatus.INACTIVE.value,
                    start_trial='stop'
                )

'''
Напоминание
- Цели 8 утра
- Состояние
рандомно с 12 до 19
- благодарность 21
- карты в 11:00 , выбрать карту
'''
