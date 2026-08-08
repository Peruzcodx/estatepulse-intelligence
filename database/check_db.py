import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "estatepulse.db"
)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Total records
cursor.execute(
    "SELECT COUNT(*) FROM property_snapshots"
)

total = cursor.fetchone()[0]

print(f"Total property snapshots: {total}")

# Count today's scrape
cursor.execute(
    """
    SELECT COUNT(*)
    FROM property_snapshots
    WHERE date(date_scraped) = '2026-08-08'
    """
)

today_count = cursor.fetchone()[0]

print(f"Properties scraped today: {today_count}")

# Show latest 10 records
cursor.execute(
    """
    SELECT title, date_scraped
    FROM property_snapshots
    ORDER BY date_scraped DESC
    LIMIT 10
    """
)

print("\nLatest records:")

for title, date_scraped in cursor.fetchall():
    print(f"{date_scraped} | {title}")

conn.close()