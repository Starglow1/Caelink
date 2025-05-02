import sqlite3

conn = sqlite3.connect('caelink.db')
conn.execute('''
    CREATE TABLE IF NOT EXISTS journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

print("Caelink journal table created successfully.")
