import sqlite3
from typing import List, Dict

DATABASE = 'photo_repo.db'

def initialize_db():
    """Initialize the database and create tables if they don't exist."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL
            )
        ''')
        conn.commit()

def save_photo_to_db(filename: str, file_path: str) -> int:
    """Save photo metadata to the database."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO photos (filename, file_path) VALUES (?, ?)',
            (filename, file_path)
        )
        conn.commit()
        return cursor.lastrowid

def list_photos_from_db() -> List[Dict[str, str]]:
    """Retrieve all photo records from the database."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, filename, file_path FROM photos')
        rows = cursor.fetchall()
        return [
            {
                'id': row[0],
                'filename': row[1],
                'file_path': row[2],
            }
            for row in rows
        ]
