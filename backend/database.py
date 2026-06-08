import sqlite3
from datetime import datetime

DB_NAME = "app.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_chat(question: str, answer: str, user_id: str = "guest"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chat_history (user_id, question, answer, created_at)
        VALUES (?, ?, ?, ?)
    """, (user_id, question, answer, datetime.now().isoformat()))

    conn.commit()
    conn.close()