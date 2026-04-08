def build_params(mode, value):
    if mode in ["keywords", "frequency"]:
        return {"n": int(value)}
    return {}