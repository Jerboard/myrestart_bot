from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


# Основная клавиатура карт
def get_main_card_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔗 Как это работает?', url=f'https://t.me/Russian_telegram_bots')
    kb.button(text='🎴 Выбрать карту', callback_data=f'get_card')
    kb.button(text='🔙 Назад', callback_data=f'account_start')
    kb.adjust (1)
    return kb.as_markup()
