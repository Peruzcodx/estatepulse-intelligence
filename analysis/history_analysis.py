import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "estatepulse.db")


def get_latest_snapshot():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM property_snapshots
    ORDER BY date_scraped DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data



def get_property_changes():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        property_id,
        title,
        price,
        availability,
        date_scraped
    FROM property_snapshots
    WHERE property_id IS NOT NULL
    ORDER BY date_scraped DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data

def get_latest_properties():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        property_id,
        title,
        price,
        availability,
        date_scraped
    FROM property_snapshots
    WHERE property_id IS NOT NULL
    ORDER BY date_scraped DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    properties = {}

    for row in rows:
        property_id = row[0]

        # keep only latest snapshot of each property
        if property_id not in properties:
            properties[property_id] = {
                "title": row[1],
                "price": row[2],
                "availability": row[3],
                "date": row[4]
            }

    return properties