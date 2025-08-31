import sqlite3
import os
from datetime import datetime

DB_PATH = "voices.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS voices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            file_path TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_voice(name, file_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO voices (name, file_path, created_at) VALUES (?, ?, ?)",
        (name, file_path, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

def list_voices():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM voices ORDER BY created_at DESC")
    voices = [row[0] for row in cursor.fetchall()]
    conn.close()
    return voices

def get_voice_path(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM voices WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
