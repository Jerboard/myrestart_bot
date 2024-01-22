from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


# Основная клавиатура дневника состояния
def get_main_attraction_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔗 Как это работает?', url=f'https://t.me/Russian_telegram_bots')
    kb.button(text='📝 Заполнить дневник', callback_data=f'add_attraction')
    kb.button(text='📚 Архив притяжений', callback_data=f'archive_attraction')
    kb.button(text='🔙 Назад', callback_data=f'account_start')
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
    kb.button(text='🌓 Отметить состояние', callback_data=f'diary_stress_check_choice')
    kb.button(text='📚 Архив состояний', callback_data=f'diary_stress_archive:global')
    kb.button(text='🔙 Назад', callback_data=f'account_start')
    kb.adjust (1)
    return kb.as_markup()


# Отметить состояние
def get_check_stress_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='😊', callback_data=f'diary_stress_check_add:1')
    kb.button(text='🙁', callback_data=f'diary_stress_check_add:0')
    kb.button(text='🔙 Назад', callback_data=f'diary_stress_main')
    kb.adjust (2, 1)
    return kb.as_markup()


# Отметить состояние
def get_archive_stress_kb(plot_type: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if plot_type == 'global':
        kb.button(text='📆 График по дням', callback_data=f'diary_stress_archive:daily')
    else:
        kb.button(text='📊 Общий график', callback_data=f'diary_stress_archive:global')
    kb.button(text='🔙 Назад', callback_data=f'diary_stress_main')
    kb.adjust (1)
    return kb.as_markup()


# Основная клавиатура дневника стресса
def get_main_thanks_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔗 Как это работает?', url=f'https://t.me/Russian_telegram_bots')
    kb.button(text='🙏 Благодарить сейчас', callback_data=f'diary_thanks_send')
    kb.button(text='📚 Мои благодарности', callback_data=f'archive_thanks')
    kb.button(text='🔙 Назад', callback_data=f'account_start')
    kb.adjust (1)
    return kb.as_markup()
