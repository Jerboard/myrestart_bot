from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType

from timezonefinder import TimezoneFinder


import db
import keyboards as kb
from init import dp, bot, DATE_FORMAT
from utils.cover_photos import get_cover_photo
from utils.data import cities_timezone
from enums import SettingCB


# даёт панель настроек
async def get_setting_main(user_id: int, message_id: int) -> None:
    user_info = await db.get_user_info (user_id)
    notify_list = []
    if user_info.notify_goal:
        notify_list.append ('goal')
    if user_info.notify_stress:
        notify_list.append ('stress')
    if user_info.notify_thank:
        notify_list.append ('thanks')
    if user_info.notify_card:
        notify_list.append ('card')

    text = (f'Управление уведомлениями\n\n'
            f'Часовой пояс: {cities_timezone[user_info.timezone]["name"]}')

    photo = InputMediaPhoto (media=get_cover_photo ('notice'), caption=text)
    await bot.edit_message_media(
        chat_id=user_id,
        message_id=message_id,
        media=photo,
        reply_markup=kb.get_main_setting_kb(notify_list))


# Настройки основное меню
@dp.callback_query(lambda cb: cb.data.startswith(SettingCB.USER_SETTINGS_MAIN.value))
async def diary_goal(cb: CallbackQuery, state: FSMContext):
    # await state.clear()

    await state.set_state ('search')
    await state.update_data (data={
        'on': 'timezone',
        'message_id': cb.message.message_id
    })

    await get_setting_main(user_id=cb.from_user.id, message_id=cb.message.message_id)


# Изменение уведомлений
@dp.callback_query(lambda cb: cb.data.startswith(SettingCB.USER_SETTINGS_NOTIFY.value))
async def diary_goal(cb: CallbackQuery, state: FSMContext):
    _, notify, action_str = cb.data.split(':')
    action = bool(int(action_str))

    if notify == 'card':
        await db.update_user_info (user_id=cb.from_user.id, notify_card=action)

    elif notify == 'goal':
        await db.update_user_info (user_id=cb.from_user.id, notify_goal=action)

    elif notify == 'stress':
        await db.update_user_info (user_id=cb.from_user.id, notify_stress=action)

    elif notify == 'thanks':
        await db.update_user_info (user_id=cb.from_user.id, notify_thank=action)

    else:
        await db.update_user_info(
            user_id=cb.from_user.id,
            notify_goal=action,
            notify_stress=action,
            notify_thank=action,
            notify_card=action
        )

    await get_setting_main (user_id=cb.from_user.id, message_id=cb.message.message_id)


# Выбор таймзоны
@dp.callback_query(lambda cb: cb.data.startswith(SettingCB.USER_SETTINGS_TZ.value))
async def diary_goal(cb: CallbackQuery, state: FSMContext):
    await state.set_state ('search')
    await state.update_data (data={
        'on': 'timezone',
        'message_id': cb.message.message_id
    })

    text = 'Отправьте свою локацию или воспользуйтесь поиском'
    await cb.message.edit_caption(caption=text, reply_markup=kb.get_search_kb(back=SettingCB.USER_SETTINGS_MAIN.value))


# Выбор таймзоны
@dp.message(lambda msg: msg.content_type == ContentType.LOCATION)
async def diary_goal(msg: Message, state: FSMContext):
    await msg.delete()
    tf = TimezoneFinder ()  # reuse

    new_tz = tf.timezone_at(lat=msg.location.latitude, lng=msg.location.longitude)
    await db.update_user_info(user_id=msg.from_user.id, timezone=new_tz)

    data = await state.get_data()
    await state.clear()

    await get_setting_main (user_id=msg.from_user.id, message_id=data['message_id'])

