from state.storage import load_data, save_data

# добавляем сообщение в историю
def add_message(user_id, role, content):
    data = load_data()

    user = data.setdefault(str(user_id), {})
    history = user.setdefault("history", [])

    history.append({
        "role": role,
        "content": content
    })

    # ограничиваем историю до 10 сообщений
    user["history"] = history[-10:]

    save_data(data)

# получаем историю сообщений
def get_history(user_id):
    data = load_data()
    return data.get(str(user_id), {}).get("history", [])