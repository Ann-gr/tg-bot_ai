from core.modes import MODE_REGISTRY, BASE_PROMPT
def create_prompt(text, mode="analysis", **kwargs):
    config = MODE_REGISTRY.get(mode, MODE_REGISTRY["analysis"])

    base_prompt = BASE_PROMPT.format(text=text)

    # добавляем историю для QA
    if mode == "qa":
        history = kwargs.get("qa_history", [])

        history_text = ""

        for item in history[-5:]:
            history_text += f"\nВопрос: {item['q']}\nОтвет: {item['a']}\n"

        if history_text:
            base_prompt += f"\n\nPREVIOUS QA:\n{history_text}"

    mode_prompt = config["prompt"].format(**kwargs)

    return base_prompt + "\n" + mode_prompt