from telegram import Update
from telegram.ext import ContextTypes

from handlers.keyboards import (
    get_mode_keyboard,
    get_param_keyboard,
    get_result_keyboard,
)
from services.analysis_service import run_analysis
from state.user_state import get_user, set_user

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    state = get_user(user_id)

    data = query.data

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
            "Выберите режим анализа:",
            reply_markup=get_mode_keyboard(),
        )
        return

    if data == "action:new_text":
        state["last_text"] = None
        set_user(user_id, state)

        await query.edit_message_text("Отправьте новый текст или файл")
        return

async def run_and_show_result(query, user_id, state):
    text = state.get("last_text")

    if not text:
        await query.edit_message_text("Сначала отправьте текст")
        return

    await query.edit_message_text("⏳ Анализирую...")

    result = await run_analysis(user_id, text, state)

    state["last_result"] = result
    set_user(user_id, state)

    await query.edit_message_text(
        result,
        reply_markup=get_result_keyboard(),
    )