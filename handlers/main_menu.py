from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.enums.message_entity_type import MessageEntityType

from datetime import datetime, timedelta
from asyncio import sleep

import pytz

import db
import keyboards as kb
from init import dp, TZ, bot
from utils.cover_photos import get_cover_photo
from enums import BaseCB, BaseState, UserStatus


# первый экран
# @dp.message(lambda msg: msg.content_type == 'photo')
# async def save_photo(msg: Message) -> None:
#     print(f'"{msg.caption}": "{msg.photo[-1].file_id}"')
    # print(f'"{msg.photo[-1].file_id}",')


# инфо при первом входе
@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.FIRST_VISIT.value))
async def first_visit(cb: CallbackQuery):
    _, step_str = cb.data.split(':')
    step = int(step_str) + 1

    photo_id = get_cover_photo ('first_visit')
    keyboard = kb.get_first_visit_kb(step)
    if step == 1:
        text = 'Текст 1'
    elif step == 2:
        text = 'Текст 2'
    elif step == 3:
        text = 'Текст 3'
    elif step == 4:
        text = 'Текст 4'
    elif step == 5:
        text = 'Текст 5'
    else:
        await db.add_user(
            user_id=cb.from_user.id,
            full_name=cb.from_user.full_name,
            username=cb.from_user.username)

        text = 'Текст 1 (то что будет написано на главном экране)'
        photo_id = get_cover_photo ('start')
        keyboard = kb.get_start_kb ()

    photo = InputMediaPhoto (media=photo_id, caption=text)
    await cb.message.edit_media (media=photo, reply_markup=keyboard)


# первый экран
@dp.message(CommandStart())
async def command_start_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    user_info = await db.get_user_info(msg.from_user.id)
    if not user_info:
        text = 'Текст 1'
        photo = get_cover_photo ('first_visit')
        keyboard = kb.get_first_visit_kb (1)

    else:
        text = 'Текст 1 (то что будет написано на главном экране)'
        photo = get_cover_photo ('start')
        keyboard = kb.get_start_kb()

    await msg.answer_photo(
        photo=photo,
        caption=text,
        protect_content=True,
        reply_markup=keyboard)


# вернуться к началу
@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.BACK_START.value))
async def back_start(cb: CallbackQuery):
    text = 'Текст 1 (то что будет написано на главном экране)'
    photo = InputMediaPhoto(media=get_cover_photo ('start'), caption=text)
    await cb.message.edit_media(media=photo, reply_markup=kb.get_start_kb())


# Пробный период инфо
@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.TRIAL_INFO.value))
async def trial_info(cb: CallbackQuery, state: FSMContext):
    user_info = await db.get_user_info (cb.from_user.id)

    if user_info.status == UserStatus.NEW.value:
        await state.set_state(BaseState.SEND_EMAIL_TRIAL.value)
        await state.update_data(data={'message_id': cb.message.message_id})

        text = ('Инфо о пробном периоде. Продолжительность 54 часа\n\n'
                'Чтоб начать пробный период отправьте адрес электронной почты')
        photo = InputMediaPhoto(media=get_cover_photo ('default'), caption=text)
        await cb.message.edit_media(media=photo, reply_markup=kb.get_back_button(BaseCB.BACK_START.value))

    elif user_info.start_trial:
        end_trial = TZ.localize(user_info.start_trial) + timedelta (hours=54)
        text = f'Тестовый период активен до {end_trial.strftime ("%H:%M %d.%m.%Y")}'

        photo = InputMediaPhoto (media=get_cover_photo ('default'), caption=text)
        await cb.message.edit_media (media=photo, reply_markup=kb.get_back_button (BaseCB.BACK_START.value))

    else:
        text = 'Тестовый период доступен только для новых подписчиков'
        await cb.answer (text, show_alert=True)


# Пробный период старт
@dp.message(StateFilter(BaseState.SEND_EMAIL_TRIAL.value))
async def send_email_trial(msg: Message, state: FSMContext) -> None:
    if msg.entities and msg.entities [0].type == MessageEntityType.EMAIL:
        start_trial = datetime.now(TZ)
        end_trial = start_trial + timedelta(hours=54)

        await db.update_user_info(
            user_id=msg.from_user.id,
            email=msg.text,
            status=UserStatus.ACTIVE.value,
            start_trial=start_trial
        )
        data = await state.get_data()
        await state.clear()

        text = f'Тестовый период активен до {end_trial.strftime("%H:%M %d.%m.%Y")}'
        photo = InputMediaPhoto (media=get_cover_photo ('default'), caption=text)
        await bot.edit_message_media (
            chat_id=msg.chat.id,
            message_id=data['message_id'],
            media=photo,
            reply_markup=kb.get_back_button (BaseCB.BACK_START.value))

    else:
        sent = await msg.answer('Некорректный адрес электронной почты')
        await sleep(3)
        await sent.delete()


# в разработке
@dp.callback_query(lambda cb: cb.data.startswith('close'))
async def in_dev(cb: CallbackQuery):
    await cb.message.delete()


# в разработке
@dp.callback_query(lambda cb: cb.data.startswith('in_dev'))
async def in_dev(cb: CallbackQuery):
    await cb.answer('🛠 Функция в разработке')


# example = {'EET': {'msk': -1, 'msk_str': '-1 час', 'utc': +2, 'utc_str': 'UTC + 2 ', 'cities': 'Калининград, Рига', 'tz': 'Europe/Moscow'}}
# cosnom_tz = '''
# Калининград (EET)	-1 час	UTC+2	Калининград, Рига
# Самара (SAMT) 	0 часов	UTC+4	Москва, Санкт-Петербург,Самара, Уфа, Казань, Челябинск, Дубай
# Екатеринбург (YEKT)	+2 часа	UTC+5	Екатеринбург, Пермь, Ульяновск, Тюмень, Ташкент, Мальдивы, Исламабад, Ашхабад
# Омск (OMST)	+3 часа	UTC+6	Омск, Новосибирск, Барнаул, Томск
# Красноярск (KRAT)	+4 часа	UTC+7	Красноярск, Иркутск, Кемерово, Новокузнецк
# Иркутск (IRKT)	+5 часов	UTC+8	Иркутск, Улан-Удэ, Чита, Братск
# Якутск (YAKT)	+6 часов	UTC+9	Якутск, Хабаровск, Чита, Благовещенск
# Владивосток (VLAT)	+7 часов	UTC+10	Владивосток, Хабаровск, Красноярск, Чита
# Магадан (MAGT)	+8 часов	UTC+11	Магадан, Южно-Сахалинск, Владивосток, Хабаровск
# Камчатка (PETT)	+9 часов	UTC+12	Петропавловск-Камчатский, Магадан, Южно-Сахалинск, Владивосток, Анадырь, Петропавловск-Камчатский, Магадан, Южно-Сахалинск
# Астана (ALMT)	+2 часа	UTC+6	Астана
# Тбилиси (GET)	+1 час	UTC+4	Тбилиси, Баку , Ереван
# Кабул (AFT)	+1.5 часа	UTC+4:30	Кабул
# Тегеран (IRST)	+1.5 часа	UTC+3:30	Тегеран
# Сидней (AEDT)	+8 часов	UTC+11	Сидней, Мельбурн, Брисбен
# Токио (JST)	+6 часов	UTC+9	Токио, Сеул, Шанхай, Гонконг
# Бангкок (ICT)	+4 часа	UTC+7	Бангкок, Джакарта, Читфо
# Дарвин (ACST)	+6.5 часа	UTC+9:30	Дарвин
# Аделаида (ACDT)	+7.5 часа	UTC+10:30	Аделаида
# Лос-Анджелес (PST)	-11 часов	UTC-8	Лос-Анджелес, Сан-Франциско, Сиэтл
# Чикаго (CST)	-9 часов	UTC-6	Чикаго, Мехико, Лима, Торонто
# Нью-Йорк (EST)	-8 часов	UTC-5	Нью-Йорк, Лима, Торонто, Ла-Хабана
# Сан-Паулу (BRT)	-6 часов	UTC-3	Сан-Паулу, Буэнос-Айрес
# Сантьяго (CLT)	-7 часов	UTC-4	Сантьяго, Ла-Пас, Буэнос-Айрес
# Анкоридж (AKST)	-12 часов	UTC-9	Анкоридж
# Гонолулу (HAST)	-14 часов	UTC-10	Гонолулу'''
#
# c = 0
# for row in cosnom_tz.split('\n'):
#     c += 1
#     print(f'{c}: {row.split("	")[1:]}')