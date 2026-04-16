# AI pipeline
from core.prompt_builder import create_prompt
from services.ai_service import analyze_with_ai
# форматирование ответа
from utils.formatter import format_response

async def run_analysis(user_id, text, state, user_question=None):
    mode = state.get("mode", "analysis")

    params = state.get("params", {})
    n = params.get("n", 10)

    MAX_AI_TEXT = 3000

    if len(text) > MAX_AI_TEXT:
        text = text[:MAX_AI_TEXT]


    # QA режим
    if mode == "qa":
        prompt = create_prompt(
            text,
            mode,
            question=user_question,
            qa_history=state.get("qa_history", [])
        )

        messages = [
            {
                "role": "system",
                "content": "Отвечай строго на русском. Только по тексту."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

    else:
        prompt = create_prompt(
            text,
            mode,
            top_n=n,
            freq_n=n
        )

        messages = [
            {
                "role": "system",
                "content": "Ты помощник по анализу текста. Отвечай на русском."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

    ai_result = await analyze_with_ai(messages)

    return format_response(ai_result, mode)