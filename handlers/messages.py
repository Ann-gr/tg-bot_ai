from telegram import Update
from telegram.ext import ContextTypes

from handlers.keyboards import get_mode_keyboard
from state.user_state import set_user, get_user

def get_default_state():
    return {
        "last_text": None,
        "mode": None,
        "params": {},
        "last_result": None
    }

# ОБРАБОТКА ТЕКСТА
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    state = get_user(user_id) or get_default_state()

    state["last_text"] = text
    set_user(user_id, state)

    await update.message.reply_text(
        "✅ Текст загружен\n\nВыберите режим анализа:",
        reply_markup=get_mode_keyboard(),
    )

# ОБРАБОТКА ФАЙЛА
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    user_id = update.effective_user.id

    state = get_user(user_id) or get_default_state()

    if not document.file_name.endswith(".txt"):
        await update.message.reply_text("Пожалуйста, отправьте .txt файл 📄")
        return

    await update.message.reply_text("📥 Загружаю файл...")

    file = await context.bot.get_file(document.file_id)
    file_path = f"/tmp/{document.file_name}"

    await file.download_to_drive(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception:
        await update.message.reply_text("❌ Не удалось загрузить файл")
        return

    if len(text) > 10000:
        text = text[:10000]

    state["last_text"] = text
    set_user(user_id, state)

    await update.message.reply_text(
        "✅ Файл загружен\n\nВыберите режим анализа:",
        reply_markup=get_mode_keyboard(),
    )