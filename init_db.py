import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'caelink.db')

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
''')

connection.commit()
connection.close()

print("Caelink database created with journal table (with timestamp).")
