import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "state.db")


def init_db():
    print("🔥 INIT DB CALLED")
    print("DB PATH:", DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_state (
        user_id TEXT PRIMARY KEY,
        state TEXT
    )
    """)

    conn.commit()
    print("✅ TABLE CREATED OR EXISTS")

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print("📦 TABLES IN DB:", cursor.fetchall())

    conn.close()