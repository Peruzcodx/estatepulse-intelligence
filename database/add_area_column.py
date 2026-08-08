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
ALTER TABLE property_snapshots
ADD COLUMN area TEXT
""")


connection.commit()

connection.close()


print("Area column added successfully")