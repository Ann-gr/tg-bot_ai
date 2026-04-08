import json
from services.db import get_pool

async def get_state_db(user_id):
    pool = await get_pool()

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT mode, params, last_text, last_result
            FROM user_state
            WHERE user_id = $1
            """,
            str(user_id)
        )

    if not row:
        return {}

    return {
        "mode": row["mode"],
        "params": json.loads(row["params"] or "{}"),
        "last_text": row["last_text"],
        "last_result": row["last_result"],
    }


async def save_state_db(user_id, state):
    pool = await get_pool()

    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO user_state (user_id, mode, params, last_text, last_result)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (user_id) DO UPDATE SET
                mode = EXCLUDED.mode,
                params = EXCLUDED.params,
                last_text = EXCLUDED.last_text,
                last_result = EXCLUDED.last_result
            """,
            str(user_id),
            state.get("mode"),
            json.dumps(state.get("params", {})),
            state.get("last_text"),
            state.get("last_result"),
        )