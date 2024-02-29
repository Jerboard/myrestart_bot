from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from utils.data import notify_map
from enums import SettingCB, BaseCB


# Основная клавиатура дневника состояния
def get_main_setting_kb(user_notify: list[str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🌐 Выбрать часовой пояс', callback_data=SettingCB.USER_SETTINGS_TZ.value)
    for k, v in notify_map.items():
        if k in user_notify:
            kb.button(text=f'🔔 {v}', callback_data=f'{SettingCB.USER_SETTINGS_NOTIFY.value}:{k}:0')
        else:
            kb.button(text=f'🔕 {v}', callback_data=f'{SettingCB.USER_SETTINGS_NOTIFY.value}:{k}:1')

    if user_notify:
        kb.button(text='🔕 Отключить все уведомления', callback_data=f'{SettingCB.USER_SETTINGS_NOTIFY.value}:all:0')
    if len(user_notify) < 4:
        kb.button(text='🔔 Включить все уведомления', callback_data=f'{SettingCB.USER_SETTINGS_NOTIFY.value}:all:1')

    kb.button (text='🔙 Назад', callback_data=BaseCB.ACCOUNT_START.value)
    return kb.adjust (1).as_markup()
