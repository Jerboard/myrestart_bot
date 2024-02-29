

tariffs = {
    '1': {'text': '1 месяц: 999 рублей', 'price': 999, 'duration': 1},
    '3': {'text': '3 месяц: 2899 рублей', 'price': 2899, 'duration': 3},
    '6': {'text': '6 месяц: 4899 рублей', 'price': 4899, 'duration': 6},
    '12': {'text': '12 месяц: 8899 рублей', 'price': 8899, 'duration': 12},
}


notify_map = {
    'card': 'Карты',
    'goal': 'Дневник Целей',
    'stress': 'Дневник состояний',
    'thanks': 'Дневник благодарностей'
}


cities_timezone = {
    'Europe/Kaliningrad': {
        'name': 'Москва -1 час (UTC +2)',
        'msk': -1,
        'msk_str': '-1 час',
        'utc': +2,
        'utc_str': 'UTC + 2',
        'cities': 'Калининград, Рига',
    },
    'Europe/Moscow': {
        'name': 'Москва +0 час (UTC +4)',
        'msk': 0,
        'msk_str': '0 часов',
        'utc': +4,
        'utc_str': 'UTC + 4',
        'cities': 'Москва, Санкт-Петербург,Самара, Уфа, Казань, Челябинск, Дубай',
    },
    'Asia/Yekaterinburg': {
        'name': 'Москва +2 час (UTC +5)',
        'msk': +2,
        'msk_str': '+2 часа',
        'utc': +5,
        'utc_str': 'UTC + 5',
        'cities': 'Екатеринбург, Пермь, Ульяновск, Тюмень, Ташкент, Мальдивы, Исламабад, Ашхабад',
    },
    'Asia/Omsk': {
        'name': 'Москва +3 час (UTC +6)',
        'msk': +3,
        'msk_str': '+3 часа',
        'utc': +6,
        'utc_str': 'UTC + 6',
        'cities': 'Омск, Новосибирск, Барнаул, Томск',
    },
    'Asia/Krasnoyarsk': {
        'name': 'Москва +4 час (UTC +7)',
        'msk': +4,
        'msk_str': '+4 часа',
        'utc': +7,
        'utc_str': 'UTC + 7',
        'cities': 'Красноярск, Иркутск, Кемерово, Новокузнецк'
    },
    'Asia/Irkutsk': {
        'name': 'Москва +5 час (UTC +8)',
        'msk': +5,
        'msk_str': '+5 часов',
        'utc': +8,
        'utc_str': 'UTC + 8',
        'cities': 'Иркутск, Улан-Удэ, Чита, Братск',
    },
    'Asia/Yakutsk': {
        'name': 'Москва +6 час (UTC +9)',
        'msk': +6,
        'msk_str': '+6 часов',
        'utc': +9,
        'utc_str': 'UTC + 9',
        'cities': 'Якутск, Хабаровск, Чита, Благовещенск'
    },
    'Asia/Vladivostok': {
        'name': 'Москва +7 час (UTC +10)',
        'msk': +7,
        'msk_str': '+7 часов',
        'utc': +10,
        'utc_str': 'UTC + 10',
        'cities': 'Владивосток, Хабаровск, Красноярск, Чита',
    },
    'Asia/Magadan': {
        'name': 'Москва +8 час (UTC +11)',
        'msk': +8,
        'msk_str': '+8 часов',
        'utc': +11,
        'utc_str': 'UTC + 11',
        'cities': 'Магадан, Южно-Сахалинск, Владивосток, Хабаровск'
    },
    'Asia/Kamchatka': {
        'name': 'Москва +9 час (UTC +12)',
        'msk': +9,
        'msk_str': '+9 часов',
        'utc': +12,
        'utc_str': 'UTC + 12',
        'cities': 'Петропавловск-Камчатский, Магадан, Южно-Сахалинск, Владивосток, Анадырь, Петропавловск-Камчатский, '
                  'Магадан, Южно-Сахалинск',
    },
    'Asia/Almaty': {
        'name': 'Москва +2 час (UTC +6)',
        'msk': +2,
        'msk_str': '+2 часа',
        'utc': +6,
        'utc_str': 'UTC + 6',
        'cities': 'Астана'
    },
    'Asia/Tbilisi': {
        'name': 'Москва +1 час (UTC +4)',
        'msk': +1,
        'msk_str': '+1 час',
        'utc': +4,
        'utc_str': 'UTC + 4',
        'cities': 'Тбилиси, Баку , Ереван'
    },
    'Asia/Kabul': {
        'name': 'Москва +1.5 час (UTC +4.5)',
        'msk': +1.5,
        'msk_str': '+1.5 часа',
        'utc': +4.5,
        'utc_str': 'UTC + 4:30',
        'cities': 'Кабул'
    },
    'Asia/Tehran': {
        'name': 'Москва +1.5 час (UTC +3.5)',
        'msk': +1.5,
        'msk_str': '+1.5 часа',
        'utc': +3.5,
        'utc_str': 'UTC + 3:30',
        'cities': 'Тегеран'
    },
    'Australia/Sydney': {
        'name': 'Москва +8 час (UTC +11)',
        'msk': +8,
        'msk_str': '+8 часов',
        'utc': +11,
        'utc_str': 'UTC + 11',
        'cities': 'Сидней, Мельбурн, Брисбен'
    },
    'Asia/Tokyo': {
        'name': 'Москва +6 час (UTC +9)',
        'msk': +6,
        'msk_str': '+6 часов',
        'utc': +9,
        'utc_str': 'UTC + 9',
        'cities': 'Токио, Сеул, Шанхай, Гонконг'
    },
    'Asia/Bangkok': {
        'name': 'Москва +4 час (UTC +7)',
        'msk': +4,
        'msk_str': '+4 часа',
        'utc': +7,
        'utc_str': 'UTC + 7',
        'cities': 'Бангкок, Джакарта, Читфо'
    },
    'Australia/Darwin': {
        'name': 'Москва +6.5 час (UTC +9.5)',
        'msk': 6.5,
        'msk_str': '+6.5 часа',
        'utc': 9.5,
        'utc_str': 'UTC+9:30',
        'cities': 'Бали, Дарвин'
    },
    'Australia/Adelaide': {
        'name': 'Москва +7.5 час (UTC +10.5)',
        'msk': 7.5,
        'msk_str': '+7.5 часа',
        'utc': 10.5,
        'utc_str': 'UTC+10:30',
        'cities': 'Аделаида'
    },
    'America/Los_Angeles': {
        'name': 'Москва -11 час (UTC -8)',
        'msk': -11,
        'msk_str': '-11 часов',
        'utc': -8,
        'utc_str': 'UTC-8',
        'cities': 'Лос-Анджелес, Сан-Франциско, Сиэтл'
    },
    'America/Chicago': {
        'name': 'Москва -9 час (UTC -6)',
        'msk': -9,
        'msk_str': '-9 часов',
        'utc': -6,
        'utc_str': 'UTC-6',
        'cities': 'Чикаго, Мехико, Лима, Торонто'
    },
    'America/New_York': {
        'name': 'Москва -8 час (UTC -5)',
        'msk': -8,
        'msk_str': '-8 часов',
        'utc': -5,
        'utc_str': 'UTC-5',
        'cities': 'Нью-Йорк, Лима, Торонто, Ла-Хабана'
    },
    'America/Sao_Paulo': {
        'name': 'Москва -6 час (UTC -3)',
        'msk': -6,
        'msk_str': '-6 часов',
        'utc': -3,
        'utc_str': 'UTC-3',
        'cities': 'Сан-Паулу, Буэнос-Айрес'
    },
    'America/Santiago': {
        'name': 'Москва -7 час (UTC -4)',
        'msk': -7,
        'msk_str': '-7 часов',
        'utc': -4,
        'utc_str': 'UTC-4',
        'cities': 'Сантьяго, Ла-Пас, Буэнос-Айрес'
    },
    'America/Anchorage': {
        'name': 'Москва -12 час (UTC -9)',
        'msk': -12,
        'msk_str': '-12 часов',
        'utc': -9,
        'utc_str': 'UTC-9',
        'cities': 'Анкоридж'
    },
    'Pacific/Honolulu': {
        'name': 'Москва -14 час (UTC -10)',
        'msk': -14,
        'msk_str': '-14 часов',
        'utc': -10,
        'utc_str': 'UTC-10',
        'cities': 'Гонолулу'
    }
}


# cities_timezone = [
#     {'tz': 'Europe/Kaliningrad',
#      'msk': -1,
#      'msk_str': '-1 час',
#      'utc': +2,
#      'utc_str': 'UTC + 2',
#      'cities': 'Калининград, Рига'
#     },
#     {'tz': 'Europe/Moscow',
#         'msk': 0,
#         'msk_str': '0 часов',
#         'utc': +4,
#         'utc_str': 'UTC + 4',
#         'cities': 'Москва, Санкт-Петербург,Самара, Уфа, Казань, Челябинск, Дубай'
#     },
#     {'tz': 'Asia/Yekaterinburg',
#         'msk': +2,
#         'msk_str': '+2 часа',
#         'utc': +5,
#         'utc_str': 'UTC + 5',
#         'cities': 'Екатеринбург, Пермь, Ульяновск, Тюмень, Ташкент, Мальдивы, Исламабад, Ашхабад'
#     },
#     {'tz': 'Asia/Omsk',
#         'msk': +3,
#         'msk_str': '+3 часа',
#         'utc': +6,
#         'utc_str': 'UTC + 6',
#         'cities': 'Омск, Новосибирск, Барнаул, Томск'
#     },
#     {'tz': 'Asia/Krasnoyarsk',
#         'msk': +4,
#         'msk_str': '+4 часа',
#         'utc': +7,
#         'utc_str': 'UTC + 7',
#         'cities': 'Красноярск, Иркутск, Кемерово, Новокузнецк'
#     },
#     {'tz': 'Asia/Irkutsk',
#         'msk': +5,
#         'msk_str': '+5 часов',
#         'utc': +8,
#         'utc_str': 'UTC + 8',
#         'cities': 'Иркутск, Улан-Удэ, Чита, Братск'
#     },
#     {'tz': 'Asia/Yakutsk',
#         'msk': +6,
#         'msk_str': '+6 часов',
#         'utc': +9,
#         'utc_str': 'UTC + 9',
#         'cities': 'Якутск, Хабаровск, Чита, Благовещенск'
#     },
#     {'tz': 'Asia/Vladivostok',
#         'msk': +7,
#         'msk_str': '+7 часов',
#         'utc': +10,
#         'utc_str': 'UTC + 10',
#         'cities': 'Владивосток, Хабаровск, Красноярск, Чита'
#     },
#     {'tz': 'Asia/Magadan',
#         'msk': +8,
#         'msk_str': '+8 часов',
#         'utc': +11,
#         'utc_str': 'UTC + 11',
#         'cities': 'Магадан, Южно-Сахалинск, Владивосток, Хабаровск'
#     },
#     {'tz': 'Asia/Kamchatka',
#         'msk': +9,
#         'msk_str': '+9 часов',
#         'utc': +12,
#         'utc_str': 'UTC + 12',
#         'cities': 'Петропавловск-Камчатский, Магадан, Южно-Сахалинск, Владивосток, Анадырь, Петропавловск-Камчатский, '
#                   'Магадан, Южно-Сахалинск'
#     },
#     {'tz': 'Asia/Almaty',
#         'msk': +2,
#         'msk_str': '+2 часа',
#         'utc': +6,
#         'utc_str': 'UTC + 6',
#         'cities': 'Астана'
#     },
#     {'tz': 'Asia/Tbilisi',
#         'msk': +1,
#         'msk_str': '+1 час',
#         'utc': +4,
#         'utc_str': 'UTC + 4',
#         'cities': 'Тбилиси, Баку , Ереван'
#     },
#     {'tz': 'Asia/Kabul',
#         'msk': +1.5,
#         'msk_str': '+1.5 часа',
#         'utc': +4.5,
#         'utc_str': 'UTC + 4:30',
#         'cities': 'Кабул'
#     },
#     {'tz': 'Asia/Tehran',
#         'msk': +1.5,
#         'msk_str': '+1.5 часа',
#         'utc': +3.5,
#         'utc_str': 'UTC + 3:30',
#         'cities': 'Тегеран'
#     },
#     {'tz': 'Australia/Sydney',
#         'msk': +8,
#         'msk_str': '+8 часов',
#         'utc': +11,
#         'utc_str': 'UTC + 11',
#         'cities': 'Сидней, Мельбурн, Брисбен'
#     },
#     {'tz': 'Asia/Tokyo',
#         'msk': +6,
#         'msk_str': '+6 часов',
#         'utc': +9,
#         'utc_str': 'UTC + 9',
#         'cities': 'Токио, Сеул, Шанхай, Гонконг'
#     },
#     {'tz': 'Asia/Bangkok',
#         'msk': +4,
#         'msk_str': '+4 часа',
#         'utc': +7,
#         'utc_str': 'UTC + 7',
#         'cities': 'Бангкок, Джакарта, Читфо'
#     },
#     {'tz': 'Australia/Darwin',
#         'msk': 6.5,
#         'msk_str': '+6.5 часа',
#         'utc': 9.5,
#         'utc_str': 'UTC+9:30',
#         'cities': 'Бали, Дарвин'
#     },
#     {'tz': 'Australia/Adelaide',
#         'msk': 7.5,
#         'msk_str': '+7.5 часа',
#         'utc': 10.5,
#         'utc_str': 'UTC+10:30',
#         'cities': 'Аделаида'
#     },
#     {'tz': 'America/Los_Angeles',
#         'msk': -11,
#         'msk_str': '-11 часов',
#         'utc': -8,
#         'utc_str': 'UTC-8',
#         'cities': 'Лос-Анджелес, Сан-Франциско, Сиэтл'
#     },
#     {'tz': 'America/Chicago',
#         'msk': -9,
#         'msk_str': '-9 часов',
#         'utc': -6,
#         'utc_str': 'UTC-6',
#         'cities': 'Чикаго, Мехико, Лима, Торонто'
#     },
#     {'tz': 'America/New_York',
#         'msk': -8,
#         'msk_str': '-8 часов',
#         'utc': -5,
#         'utc_str': 'UTC-5',
#         'cities': 'Нью-Йорк, Лима, Торонто, Ла-Хабана'
#     },
#     {'tz': 'America/Sao_Paulo',
#         'msk': -6,
#         'msk_str': '-6 часов',
#         'utc': -3,
#         'utc_str': 'UTC-3',
#         'cities': 'Сан-Паулу, Буэнос-Айрес'
#     },
#     {'tz': 'America/Santiago',
#         'msk': -7,
#         'msk_str': '-7 часов',
#         'utc': -4,
#         'utc_str': 'UTC-4',
#         'cities': 'Сантьяго, Ла-Пас, Буэнос-Айрес'
#     },
#     {'tz': 'America/Anchorage',
#         'msk': -12,
#         'msk_str': '-12 часов',
#         'utc': -9,
#         'utc_str': 'UTC-9',
#         'cities': 'Анкоридж'
#     },
#     {'tz': 'Pacific/Honolulu',
#         'msk': -14,
#         'msk_str': '-14 часов',
#         'utc': -10,
#         'utc_str': 'UTC-10',
#         'cities': 'Гонолулу'
#     }
# ]
