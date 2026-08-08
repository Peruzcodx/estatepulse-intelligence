import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(
    BASE_DIR,
    "estatepulse.db"
)


connection = sqlite3.connect(DB_PATH)

cursor = connection.cursor()


cursor.execute("""
SELECT location, area
FROM property_snapshots
LIMIT 10
""")


results = cursor.fetchall()


for row in results:
    print(row)


connection.close()