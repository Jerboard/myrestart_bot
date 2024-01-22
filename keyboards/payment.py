from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from utils.data import tariffs


# Стартовая клавиатура
def get_tariff_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for k, v in tariffs.items():
        kb.button(text=v['text'], callback_data=f'payment_tariff:{k}')
    kb.button(text='🔙 Назад', callback_data=f'back_start')
    kb.adjust (1)
    return kb.as_markup()


# Стартовая клавиатура
def get_payment_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=f'Перейти на страницу оплаты', url=f'https://prodamus.ru/')
    kb.button(text='Я оплатил', callback_data=f'payment_confirm')
    kb.adjust (1)
    return kb.as_markup()


# Клавиатура после оплаты
def get_end_payment_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=f'🗂 Перейти в личный кабинет', callback_data=f'account_start')
    kb.button(text='🔙 Вернуться на главный экран', callback_data=f'back_start')
    kb.adjust (1)
    return kb.as_markup()
