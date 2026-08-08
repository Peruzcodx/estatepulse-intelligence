import sqlite3

connection = sqlite3.connect("database/estatepulse.db")

cursor = connection.cursor()

cursor.execute("""
SELECT *
FROM property_snapshots
ORDER BY id DESC
LIMIT 5
""")

records = cursor.fetchall()

for record in records:
    print(record)

connection.close()