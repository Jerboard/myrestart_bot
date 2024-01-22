from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


# универсальная кнопка назад
def get_back_button(callback: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (text='🔙 Назад', callback_data=callback)
    return kb.as_markup()


# Стартовая клавиатура
def get_start_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🗂 Личный кабинет', callback_data=f'account_start')
    kb.button(text='🔗 О проекте', url=f'https://t.me/Russian_telegram_bots')
    kb.button(text='💳 Перейти к оплате', callback_data=f'start_payment')
    kb.button(text='Служба заботы', callback_data=f'in_dev')
    kb.button(text='Пробный период', callback_data=f'in_dev')
    kb.adjust (1)
    return kb.as_markup()


# Основная клавиатура аккаунта
def get_main_account_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔗 Как это работает?', url=f'https://t.me/Russian_telegram_bots')
    kb.button(text='📘 Дневник притяжений', callback_data=f'diary_attraction_main')
    kb.button(text='📕 Дневник напряжений', callback_data=f'diary_stress_main')
    kb.button(text='📗 Дневник благодарности', callback_data=f'diary_thanks_main')
    kb.button(text='🎴 Работа с картами', callback_data=f'cards_main')
    kb.button(text='⚙️ Настройка уведомлений', callback_data=f'in_dev')
    kb.button(text='🔙 Назад', callback_data=f'back_start')
    kb.adjust (1)
    return kb.as_markup()


# если не оплатил лк
def get_account_not_active_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (text='💳 Перейти к оплате', callback_data='start_payment')
    kb.button (text='🔙 Назад', callback_data='back_start')
    kb.adjust (1)
    return kb.as_markup()
