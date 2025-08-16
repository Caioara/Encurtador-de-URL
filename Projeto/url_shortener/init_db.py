import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.executescript("""
DROP TABLE IF EXISTS urls;
CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_url TEXT NOT NULL,
    short_id TEXT UNIQUE NOT NULL,
    criador TEXT NOT NULL,
    data_criacao TEXT NOT NULL
);
""")
conn.commit()
conn.close()

print("Banco de dados criado com sucesso.")
