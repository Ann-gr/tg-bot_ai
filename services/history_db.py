from services.db import get_pool

async def add_message_db(user_id, role, content):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO history (user_id, role, content)
            VALUES ($1, $2, $3)
            """,
            str(user_id), role, content
        )

async def get_history_db(user_id, limit=6):
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT role, content
            FROM history
            WHERE user_id = $1
            ORDER BY id DESC
            LIMIT $2
            """,
            str(user_id),
            limit
        )

    return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]