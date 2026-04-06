import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "state.db")

def init_db():
    print("🔥 INIT DB CALLED")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # пересоздаём таблицу
    cursor.execute("DROP TABLE IF EXISTS user_state")

    cursor.execute("""
    CREATE TABLE user_state (
        user_id TEXT PRIMARY KEY,
        mode TEXT,
        params TEXT,
        last_text TEXT,
        last_result TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        role TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    print("✅ TABLES CREATED")

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print("📦 TABLES:", cursor.fetchall())

    conn.close()