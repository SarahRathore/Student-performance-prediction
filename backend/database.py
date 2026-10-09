import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "student_predictions.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        predicted_score REAL,
        performance TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

        connection.commit()
    finally:
        connection.close()


def save_prediction(predicted_score, performance):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO predictions (predicted_score, performance)
            VALUES (?, ?)
            """,
            (predicted_score, performance)
        )

        connection.commit()
    finally:
        connection.close()


def get_predictions():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, predicted_score, performance
            FROM predictions
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()
        return rows

    finally:
        connection.close()


def delete_predictions():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("DELETE FROM predictions")
        cursor.execute(
            "DELETE FROM sqlite_sequence WHERE name='predictions'"
        )

        connection.commit()
    finally:
        connection.close()

def add_input_data_column():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("PRAGMA table_info(predictions)")
        columns = [row[1] for row in cursor.fetchall()]

        if "input_data" not in columns:
            cursor.execute("""
                ALTER TABLE predictions
                ADD COLUMN input_data TEXT
            """)

            connection.commit()

    finally:
        connection.close()

if __name__ == "__main__":
    init_db()
    add_input_data_column()
    print("Database updated successfully!")
