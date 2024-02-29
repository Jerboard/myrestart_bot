from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from enums import SettingCB, BaseCB


# универсальная кнопка назад
def get_back_button(callback: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (text='🔙 Назад', callback_data=callback)
    return kb.as_markup()


# универсальная кнопка назад
def get_first_visit_kb(step: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (text='✔️ Дальше', callback_data=f'{BaseCB.FIRST_VISIT.value}:{step}')
    return kb.as_markup()


# Стартовая клавиатура
def get_start_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🗂 Личный кабинет', callback_data=f'account_start')
    kb.button(text='🔗 О проекте', url=f'https://t.me/Russian_telegram_bots')
    kb.button(text='💳 Перейти к оплате', callback_data=f'start_payment')
    kb.button(text='Служба заботы', callback_data=f'in_dev')
    kb.button(text='Пробный период', callback_data=BaseCB.TRIAL_INFO.value)
    kb.adjust (1)
    return kb.as_markup()


# Основная клавиатура аккаунта
def get_main_account_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔗 Как это работает?', url=f'https://t.me/Russian_telegram_bots')
    kb.button(text='📘 Дневник целей', callback_data=f'diary_goal_main')
    kb.button(text='📕 Дневник напряжений', callback_data=f'diary_stress_main')
    kb.button(text='📗 Дневник благодарности', callback_data=f'diary_thanks_main')
    kb.button(text='🎴 Работа с картами', callback_data=f'cards_main')
    kb.button(text='⚙️ Настройка уведомлений', callback_data=SettingCB.USER_SETTINGS_MAIN.value)
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


# Начать тестовый период
def get_start_trial_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (text='Начать тестовый период', callback_data=BaseCB.TRIAL_START.value)
    kb.button (text='🔙 Назад', callback_data='back_start')
    kb.adjust (1)
    return kb.as_markup()


# клавиатура напоминаний
def get_notify_kb(notify_type: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if notify_type == 'goal':
        kb.button (text='📝 Заполнить дневник', callback_data=f'add_goal')
    elif notify_type == 'stress':
        kb.button(text='🌓 Отметить состояние', callback_data=f'diary_stress_check_choice')
    elif notify_type == 'thank':
        kb.button(text='🙏 Благодарить сейчас', callback_data=f'diary_thanks_send')
    elif notify_type == 'card':
        kb.button(text='🎴 Выбрать карту', callback_data=f'get_card')
    kb.button(text='🔙 Назад', callback_data=f'close')
    return kb.adjust (1).as_markup()