import sqlite3

DB_NAME = "tea.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        origin TEXT,
        color TEXT,
        description TEXT,
        aromas TEXT,
        smell_rating INTEGER,
        taste_rating INTEGER,
        temperature INTEGER,
        duration INTEGER,
        container TEXT,
        keywords TEXT,
        technical TEXT,
        personal_notes TEXT,
        status TEXT          
    )
    """)

    conn.commit()
    conn.close()
