from core.modes import MODE_REGISTRY, BASE_PROMPT
def create_prompt(text, mode="analysis", **kwargs):
    config = MODE_REGISTRY.get(mode)

    if not config:
        config = MODE_REGISTRY["analysis"]

    prompt = BASE_PROMPT.format(text=text)

    mode_prompt = config["prompt"].format(**kwargs)

    return prompt + "\n" + mode_prompt