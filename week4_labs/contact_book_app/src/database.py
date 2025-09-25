# database.py
import sqlite3
from typing import Optional

def init_db(db_name: str = 'contacts.db'):
    """Initializes the database and creates the contacts table if it doesn't exist."""
    conn = sqlite3.connect(db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    return conn

def add_contact_db(conn, name: str, phone: Optional[str], email: Optional[str]):
    """Adds a new contact to the database."""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
        (name, phone, email)
    )
    conn.commit()

def get_all_contacts_db(conn, search_term: Optional[str] = None):
    """Retrieves all contacts from the database, with optional filtering."""
    cursor = conn.cursor()
    if search_term:
        cursor.execute(
            "SELECT id, name, phone, email FROM contacts WHERE name LIKE ?",
            (f'%{search_term}%',)
        )
    else:
        cursor.execute("SELECT id, name, phone, email FROM contacts")
    return cursor.fetchall()

def update_contact_db(conn, contact_id: int, name: str, phone: Optional[str], email: Optional[str]):
    """Updates an existing contact in the database."""
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?",
        (name, phone, email, contact_id)
    )
    conn.commit()

def delete_contact_db(conn, contact_id: int):
    """Deletes a contact from the database."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()