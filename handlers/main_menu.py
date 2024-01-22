from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

import db
import keyboards as kb
from init import dp
from utils.cover_photos import get_cover_photo


# первый экран
# @dp.message(lambda msg: msg.content_type == 'photo')
# async def save_photo(msg: Message) -> None:
#     print(f'"{msg.caption}": "{msg.photo[-1].file_id}"')
    # print(f'"{msg.photo[-1].file_id}",')


# первый экран
@dp.message(CommandStart())
async def command_start_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    user_info = await db.get_user_info(msg.from_user.id)
    if not user_info:
        await db.add_user(
            user_id=msg.from_user.id,
            full_name=msg.from_user.full_name,
            username=msg.from_user.username)

    text = 'Текст 1 (то что будет написано на главном экране)'
    await msg.answer_photo(photo=get_cover_photo ('start'), caption=text, reply_markup=kb.get_start_kb())


# в разработке
@dp.callback_query(lambda cb: cb.data.startswith('back_start'))
async def back_start(cb: CallbackQuery):
    text = 'Текст 1 (то что будет написано на главном экране)'
    photo = InputMediaPhoto(media=get_cover_photo ('start'), caption=text)
    await cb.message.edit_media(media=photo, reply_markup=kb.get_start_kb())


# в разработке
@dp.callback_query(lambda cb: cb.data.startswith('in_dev'))
async def in_dev(cb: CallbackQuery):
    await cb.answer('🛠 Функция в разработке')
