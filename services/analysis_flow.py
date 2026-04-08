from services.analysis_service import run_analysis

async def process_analysis(user_id, state):
    text = state.get("last_text")
    mode = state.get("mode")

    if not text:
        return {
            "error": "Сначала отправьте текст",
            "result": None
        }
    
    if mode == "qa":
        question = state.get("question")

        if not question:
            return {
                "error": "Введите вопрос по тексту",
                "result": None
            }

    result = await run_analysis(user_id, text, state)

    return {
        "error": None,
        "result": result
    }