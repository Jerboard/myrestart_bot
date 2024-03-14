from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from enums import DiaryCB, BaseCB


# Основная клавиатура дневника состояния
def get_main_goal_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔗 Как это работает?', url=f'https://t.me/Russian_telegram_bots')
    kb.button(text='📝 Заполнить дневник', callback_data=DiaryCB.ADD_GOAL.value)
    kb.button(text='📚 Архив целей', callback_data=DiaryCB.ARCHIVE_GOAL.value)
    kb.button(text='🔙 Назад', callback_data=BaseCB.ACCOUNT_START.value)
    kb.adjust (1)
    return kb.as_markup()


# Поиск по притяжениям
def get_search_kb(back: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (text='🔍 Поиск', switch_inline_query_current_chat='')
    kb.button (text='🔙 Назад', callback_data=back)
    kb.adjust (1)
    return kb.as_markup()


# Основная клавиатура дневника стресса
def get_main_stress_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔗 Как это работает?', url=f'https://t.me/Russian_telegram_bots')
    kb.button(text='🌓 Отметить состояние', callback_data=DiaryCB.DIARY_STRESS_CHECK_CHOICE.value)
    kb.button(text='📚 Архив состояний', callback_data=f'{DiaryCB.DIARY_STRESS_ARCHIVE.value}:global')
    kb.button(text='🔙 Назад', callback_data=BaseCB.ACCOUNT_START.value)
    kb.button (text='📆 График по дням', callback_data=f'{DiaryCB.DIARY_STRESS_ARCHIVE.value}:daily')
    kb.adjust (1)
    return kb.as_markup()


# Отметить состояние
def get_check_stress_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='😊 Расслабленное', callback_data=f'{DiaryCB.DIARY_STRESS_CHECK_ADD.value}:1')
    kb.button(text='🙁 Напряжённое', callback_data=f'{DiaryCB.DIARY_STRESS_CHECK_ADD.value}:0')
    kb.button(text='🔙 Назад', callback_data=DiaryCB.DIARY_STRESS_MAIN.value)
    kb.adjust (2, 1)
    return kb.as_markup()


# Отметить состояние
def get_archive_stress_kb(plot_type: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if plot_type == 'global':
        kb.button(text='📆 График по дням', callback_data=f'{DiaryCB.DIARY_STRESS_ARCHIVE.value}:daily')
    else:
        kb.button(text='📊 Общий график', callback_data=f'{DiaryCB.DIARY_STRESS_ARCHIVE.value}:global')
    kb.button(text='🔙 Назад', callback_data=DiaryCB.DIARY_STRESS_MAIN.value)
    kb.adjust (1)
    return kb.as_markup()


# Основная клавиатура дневника стресса
def get_main_thanks_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔗 Как это работает?', url=f'https://t.me/Russian_telegram_bots')
    kb.button(text='🙏 Благодарить сейчас', callback_data=DiaryCB.DIARY_THANKS_SEND.value)
    kb.button(text='📚 Мои благодарности', callback_data=DiaryCB.ARCHIVE_THANKS.value)
    kb.button(text='🔙 Назад', callback_data=BaseCB.ACCOUNT_START.value)
    kb.adjust (1)
    return kb.as_markup()
