import enum


class UserStatus(str, enum.Enum):
    NEW = 'new'
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class BaseState(str, enum.Enum):
    SEND_EMAIL_TRIAL = 'send_email_trial'
