from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Начать анкету", callback_data="start_form")]
    ])


def education_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1️⃣ Школа")],
            [KeyboardButton(text="2️⃣ Колледж / техникум")],
            [KeyboardButton(text="3️⃣ Университет")],
            [KeyboardButton(text="4️⃣ Уже работаю")],
        ],
        resize_keyboard=True
    )


def work_format_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1️⃣ Удалёнка 💻")],
            [KeyboardButton(text="2️⃣ Офис 🏢")],
            [KeyboardButton(text="3️⃣ Без разницы 🔄")],
        ],
        resize_keyboard=True
    )


def goal_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1️⃣ Подработка 💸")],
            [KeyboardButton(text="2️⃣ Первый опыт 🧠")],
            [KeyboardButton(text="3️⃣ Карьера 🚀")],
            [KeyboardButton(text="4️⃣ Просто попробовать 👀")],
        ],
        resize_keyboard=True
    )