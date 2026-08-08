import sqlite3
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "estatepulse.db"
)

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("""
    SELECT
        property_id,
        title,
        bedroom,
        bathroom,
        size,
        apartment_type,
        availability
    FROM property_snapshots
    WHERE
        LOWER(title) LIKE '%land%'
        OR LOWER(apartment_type) LIKE '%land%'
        OR LOWER(bedroom) LIKE '%land%'
        OR LOWER(bathroom) LIKE '%land%'
""")

rows = cursor.fetchall()

conn.close()


print("\nLAND RECORDS FOUND:")
print("=" * 80)

for row in rows:

    print(f"""
Property ID: {row[0]}
Title: {row[1]}
Bedroom: {row[2]}
Bathroom: {row[3]}
Size: {row[4]}
Type: {row[5]}
Availability: {row[6]}
""")

print("=" * 80)
print(f"Total matching records: {len(rows)}")