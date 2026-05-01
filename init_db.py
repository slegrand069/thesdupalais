from db import get_connection

conn = get_connection()
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS teas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    origin TEXT,
    color TEXT,
    description TEXT,
    aromas TEXT,
    smell_rating INTEGER DEFAULT 0,
    taste_rating INTEGER DEFAULT 0,
    temperature INTEGER DEFAULT 70,
    duration INTEGER DEFAULT 3,
    container TEXT,
    keywords TEXT,
    technical TEXT,
    personal_notes TEXT,
    status TEXT DEFAULT 'Disponible',
    badges TEXT
)
""")
conn.commit()
conn.close()

print("DB OK")