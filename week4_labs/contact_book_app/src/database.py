# database.py
import sqlite3

def init_db():
    """Initializes DB and ensures contacts table exists."""
    conn = sqlite3.connect("contacts.db", check_same_thread=False)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            phone TEXT,
            email TEXT
        )
        """
    )
    conn.commit()
    return conn

def add_contact_db(conn, name, phone, email):
    """
    Adds a new contact.
    Returns True on success, False if a contact with the same name exists.
    """
    cur = conn.cursor()
    # Simple duplicate-name check (name uniqueness enforced by DB too)
    cur.execute("SELECT 1 FROM contacts WHERE LOWER(name) = LOWER(?)", (name.strip(),))
    if cur.fetchone():
        return False
    cur.execute(
        "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
        (name.strip(), phone.strip(), email.strip())
    )
    conn.commit()
    return True

def get_all_contacts_db(conn, search_term=""):
    """
    Retrieves all contacts sorted alphabetically by name.
    If search_term provided, filters by name.
    """
    cur = conn.cursor()
    if search_term:
        cur.execute(
            "SELECT id, name, phone, email FROM contacts WHERE name LIKE ? ORDER BY LOWER(name)",
            (f"%{search_term}%",)
        )
    else:
        cur.execute("SELECT id, name, phone, email FROM contacts ORDER BY LOWER(name)")
    return cur.fetchall()

def update_contact_db(conn, contact_id, name, phone, email):
    """Update existing contact. Returns True if updated, False if name conflicts with another contact."""
    cur = conn.cursor()
    # Check name conflict: another record (different id) with same name (case-insensitive)
    cur.execute("SELECT id FROM contacts WHERE LOWER(name)=LOWER(?) AND id<>?", (name.strip(), contact_id))
    conflict = cur.fetchone()
    if conflict:
        return False
    cur.execute(
        "UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?",
        (name.strip(), phone.strip(), email.strip(), contact_id)
    )
    conn.commit()
    return True

def delete_contact_db(conn, contact_id):
    """Deletes a contact by id."""
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()