MODE_TITLES = {
    "analysis": "📊 Общий анализ",
    "summary": "📝 Краткое содержание",
    "keywords": "🔑 Ключевые слова",
    "frequency": "📈 Частотный анализ",
    "sentiment": "🧠 Тональность",
    "qa": "❓ Вопрос по тексту"
}

def get_mode_title(mode: str) -> str:
    return MODE_TITLES.get(mode, "📊 Анализ")