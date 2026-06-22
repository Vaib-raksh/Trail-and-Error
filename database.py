import sqlite3

conn = sqlite3.connect("aaharwise.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        food TEXT NOT NULL,
        time TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")
cursor.execute("""
    INSERT INTO users (name, age) VALUES (?, ?)
""", ("Vaibhavi", 21))

user_id = cursor.lastrowid

cursor.execute("""
    INSERT INTO meals (user_id, food, time) VALUES (?, ?, ?)
""", (user_id, "rice, dal, sabzi", "2026-06-22 13:00"))

conn.commit()
print(f"Added user with id: {user_id}")

conn.commit()
print("Database created successfully")