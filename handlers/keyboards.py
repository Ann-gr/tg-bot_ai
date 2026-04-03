from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_mode_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📊 Общий анализ", callback_data="mode:analysis"),
            InlineKeyboardButton("📝 Краткое содержание", callback_data="mode:summary"),
        ],
        [
            InlineKeyboardButton("🔑 Ключевые слова", callback_data="mode:keywords"),
            InlineKeyboardButton("📈 Частотный анализ", callback_data="mode:frequency"),
        ],
        [
            InlineKeyboardButton("🧠 Тональность", callback_data="mode:sentiment"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_param_keyboard(mode):
    values = [5, 10, 20, 50]

    keyboard = [
        [InlineKeyboardButton(str(v), callback_data=f"param:{mode}:{v}")]
        for v in values
    ]

    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="action:change_mode")])

    return InlineKeyboardMarkup(keyboard)

def get_result_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🔁 Повторить", callback_data="action:repeat"),
        ],
        [
            InlineKeyboardButton("⚙️ Изменить режим", callback_data="action:change_mode"),
            InlineKeyboardButton("🆕 Новый текст", callback_data="action:new_text"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)