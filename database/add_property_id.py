import sqlite3

connection = sqlite3.connect("database/estatepulse.db")

cursor = connection.cursor()

cursor.execute("""
ALTER TABLE property_snapshots
ADD COLUMN property_id TEXT
""")

connection.commit()

connection.close()

print("property_id column added successfully")