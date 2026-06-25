import sqlite3

conn = sqlite3.connect("aaharwise.db", check_same_thread=False)
cursor = conn.cursor()

# create tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER
    )""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        food TEXT NOT NULL,
        time TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")

conn.commit()

def add_user(name, age):
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    return cursor.lastrowid

def add_meal(user_id, food, time):
    cursor.execute("INSERT INTO meals (user_id, food, time) VALUES (?, ?, ?)", (user_id, food, time))
    conn.commit()

def get_meals(user_id):
    cursor.execute("""
        SELECT meals.food, meals.time, users.name 
        FROM meals 
        JOIN users ON meals.user_id = users.id
        WHERE meals.user_id = ?
    """, (user_id,))
    return cursor.fetchall()

if __name__ == "__main__":
    user_id = add_user("Vaibhavi", 21)
    add_meal(user_id, "rice, dal, sabzi", "2026-06-23 13:00")
    add_meal(user_id, "banana, milk", "2026-06-23 08:00")

    meals = get_meals(user_id)
    for meal in meals:
        print(f"{meal[2]} ate {meal[0]} at {meal[1]}")
