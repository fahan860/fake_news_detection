import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

from ..config import DB_PATH


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              username TEXT NOT NULL,
                              email TEXT NOT NULL UNIQUE,
                              password TEXT NOT NULL)"""
        )
        conn.commit()


def get_user_by_email(email: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cursor.fetchone()


def create_user(username: str, email: str, password: str) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            return False

        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password),
        )
        conn.commit()
        return True


def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if user and check_password_hash(user[3], password):
        return user
    return None
