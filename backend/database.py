import sqlite3

connection = sqlite3.connect("student_predictions.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    predicted_score REAL,
    performance TEXT
)
""")

connection.commit()

connection.close()

print("Database created successfully!")
def save_prediction(predicted_score, performance):
    connection = sqlite3.connect("student_predictions.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO predictions (predicted_score, performance) VALUES (?, ?)",
        (predicted_score, performance)
    )

    connection.commit()
    connection.close()