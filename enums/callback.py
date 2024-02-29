import enum


class BaseCB(str, enum.Enum):
    FIRST_VISIT = 'first_visit'
    BACK_START = 'back_start'
    ACCOUNT_START = 'account_start'
    TRIAL_INFO = 'trial_info'
    TRIAL_START = 'trial_start'


class SettingCB(str, enum.Enum):
    USER_SETTINGS_MAIN = "user_settings_main"
    USER_SETTINGS_NOTIFY = "user_settings_notify"
    USER_SETTINGS_TZ = "user_settings_tz"


class DiaryCB(str, enum.Enum):
    DIARY_GOAL_MAIN = "diary_goal_main"
    ARCHIVE_GOAL = "archive_goal"
    ADD_GOAL = "add_goal"
    DIARY_STRESS_MAIN = "diary_stress_main"
    DIARY_STRESS_CHECK_CHOICE = "diary_stress_check_choice"
    DIARY_STRESS_CHECK_ADD = "diary_stress_check_add"
    DIARY_STRESS_ARCHIVE = "diary_stress_archive"
    DIARY_THANKS_MAIN = "diary_thanks_main"
    DIARY_THANKS_SEND = "diary_thanks_send"
    ARCHIVE_THANKS = "archive_thanks"
