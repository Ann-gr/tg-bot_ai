from telegram import Update
from telegram.ext import ContextTypes

from handlers.keyboards import (
    get_mode_keyboard,
    get_param_keyboard,
    get_result_keyboard,
    get_main_menu_keyboard,
    get_back_keyboard,
)
from services.analysis_service import run_analysis
from state.user_state import get_user, set_user
from utils.text_utils import shorten_text
from utils.mode_utils import get_mode_title

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    state = get_user(user_id)

    data = query.data

    # UI навигация
    if data == "go:menu":
        state["screen"] = "MAIN_MENU"
        set_user(user_id, state)
        has_text = bool(state.get("last_text"))
        mode_title = get_mode_title(state.get("mode"))

        await query.edit_message_text(
            "📊 Главное меню\n\n"
            f"Текущий режим: {mode_title}\n\n"
            "Выберите действие:",
            reply_markup=get_main_menu_keyboard(has_text)
        )
        return

    elif data == "go:upload":
        state["screen"] = "UPLOAD"
        set_user(user_id, state)

        await query.edit_message_text(
            "📂 Отправьте текст или файл",
            reply_markup=get_back_keyboard()
        )
        return

    elif data == "go:help":
        state["screen"] = "HELP"
        set_user(user_id, state)

        await query.edit_message_text(
            "🧠 *Режимы анализа*\n\n"
            "📊 *Общий анализ*\n"
            "→ краткое содержание, тема, ключевые идеи\n\n"
            "📝 *Краткое содержание*\n"
            "→ выжимка текста в 2–4 предложения\n\n"
            "🔑 *Ключевые слова*\n"
            "→ самые важные слова (вы выбираете количество)\n\n"
            "📈 *Частотный анализ*\n"
            "→ какие слова встречаются чаще всего\n\n"
            "🧠 *Тональность*\n"
            "→ позитивный / нейтральный / негативный\n\n"
            "📌 Как это работает:\n"
            "1. Отправьте файл или текст\n"
            "2. Выберите режим\n"
            "3. Получите анализ\n"
            "4. При необходимости — измените режим без повторной загрузки",
            parse_mode="Markdown",
            reply_markup=get_back_keyboard()
        )
        return
    
    elif data == "go:example":
        state["screen"] = "EXAMPLE"
        set_user(user_id, state)

        await query.edit_message_text(
            "📌 Пример работы:\n\n"
            "Вы отправляете:\n"
            "📄 PDF со статьёй\n\n"
            "Выбираете:\n"
            "📝 Краткое содержание\n\n"
            "Я возвращаю:\n"
            "• Основную мысль\n"
            "• Ключевые выводы\n"
            "• Короткое резюме",
            reply_markup=get_back_keyboard()
        )
        return

    if data.startswith("mode:"):
        mode = data.split(":")[1]
        state["mode"] = mode
        set_user(user_id, state)

        if mode in ["keywords", "frequency"]:
            await query.edit_message_text(
                "Выберите количество:",
                reply_markup=get_param_keyboard(mode),
            )
            return

        await run_and_show_result(query, user_id, state)
        return

    if data.startswith("param:"):
        _, mode, value = data.split(":")
        state["mode"] = mode
        state["params"] = {"n": int(value)}
        set_user(user_id, state)

        await run_and_show_result(query, user_id, state)
        return

    if data == "action:repeat":
        await run_and_show_result(query, user_id, state)
        return

    if data == "action:change_mode":
        await query.edit_message_text(
            "⚙️ Выберите новый режим анализа:",
            reply_markup=get_mode_keyboard(),
        )
        return

    if data == "action:new_text":
        state["last_text"] = None
        set_user(user_id, state)

        await query.edit_message_text(
            "📂 Отправьте новый текст или файл", 
            reply_markup=get_back_keyboard())
        return
    
    if data == "action:full_result":
        full_text = state.get("last_result", "")

        if not full_text:
            await query.edit_message_text("❌ Нет результата")
            return
        
        title = get_mode_title(state.get("mode"))

        await query.edit_message_text(
            f"{title}\n\n{full_text}",
            reply_markup=get_result_keyboard(False),
        )
        return

async def run_and_show_result(query, user_id, state):
    text = state.get("last_text")

    if not text:
        await query.edit_message_text("Сначала отправьте текст")
        return

    await query.edit_message_text("⏳ Анализирую...\n\nЭто может занять несколько секунд")

    result = await run_analysis(user_id, text, state)

    state["last_result"] = result
    set_user(user_id, state)

    title = get_mode_title(state.get("mode"))

    short_text, is_truncated = shorten_text(result)

    formatted_text = (
        f"{title}\n\n"
        f"{short_text}\n\n"
    )

    if is_truncated:
        formatted_text += "👇 Нажмите, чтобы посмотреть полностью"

    await query.edit_message_text(
        formatted_text,
        reply_markup=get_result_keyboard(is_truncated),
    )