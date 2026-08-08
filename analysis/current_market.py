import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "estatepulse.db"
)


def get_current_properties():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM property_snapshots
    WHERE id IN (
        SELECT MAX(id)
        FROM property_snapshots
        GROUP BY property_id
    )
    """)

    properties = cursor.fetchall()

    conn.close()

    return properties