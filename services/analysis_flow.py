from services.analysis_service import run_analysis
from services.text_repository import get_text, save_text
from services.analysis_repository import save_analysis
from services.qa_repository import save_qa
from state import state_manager

async def handle_qa(user_id, state, question):
    if not state.get("current_text_id"):
        return {"error": "Сначала отправьте текст"}

    text = await get_text(state["current_text_id"])

    result = await run_analysis(
        user_id,
        text,
        state,
        user_question=question
    )

    # сохраняем историю
    qa_history = state.get("qa_history", [])
    qa_history.append({"q": question, "a": result})
    state["qa_history"] = qa_history[-5:]  # уменьшаем до 5

    await save_qa(user_id, state["current_text_id"], question, result)
    await state_manager.update_state(user_id, **state)

    return {
        "action": "show_result",
        "result": result,
        "result_id": None,  # важно!
        "state": state
    }

async def process_user_input(user_id, state, new_text=None, user_question=None):
    if state.get("mode") == "qa":
        if not user_question:
            return {"error": "❓ Введите вопрос"}

        return await handle_qa(user_id, state, user_question)
    
    # если пришёл новый текст
    elif new_text:
        text_id = await save_text(user_id, new_text)

        state["current_text_id"] = text_id

        return {
            "action": "ask_mode",
            "state": state
        }

    # если текста нет
    if not state.get("current_text_id"):
        return {"error": "❌ Сначала отправьте текст"}

    # достаём текст
    text = await get_text(state["current_text_id"])
    
    result = await run_analysis(user_id, text, state)

    analysis_id = await save_analysis(
        user_id,
        state["current_text_id"],
        state["mode"],
        result
    )

    return {
        "action": "show_result",
        "result": result,
        "result_id": analysis_id,
        "state": state
    }