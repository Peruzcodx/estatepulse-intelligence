import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(
    BASE_DIR,
    "estatepulse.db"
)


connection = sqlite3.connect(DB_PATH)

cursor = connection.cursor()


cursor.execute(
    "PRAGMA table_info(property_snapshots)"
)

columns = cursor.fetchall()


print("Property Snapshot Columns:\n")

for column in columns:
    print(column)


connection.close()