from telegram import InlineKeyboardButton

language_keyboard = [
    [
        InlineKeyboardButton("Русский", callback_data="ru"),
        InlineKeyboardButton("English", callback_data="en"),
    ]
]

action_keyboard_ru = [[InlineKeyboardButton("Заполнить анкету")]]
action_keyboard = [[InlineKeyboardButton("Fill out the form")]]

set_geo_keyboard_ru = [
    [
        InlineKeyboardButton("Индия"),
        InlineKeyboardButton("Бангладеш"),
        InlineKeyboardButton("Турция"),
    ],
    [
        InlineKeyboardButton("Канада"),
        InlineKeyboardButton("Узбекистан"),
        InlineKeyboardButton("Казахстан"),
    ],
]
set_geo_keyboard = [
    [
        InlineKeyboardButton("India"),
        InlineKeyboardButton("Bangladesh"),
        InlineKeyboardButton("Türkiye"),
    ],
    [
        InlineKeyboardButton("Canada"),
        InlineKeyboardButton("Uzbekistan"),
        InlineKeyboardButton("Kazakhstan"),
    ],
]
