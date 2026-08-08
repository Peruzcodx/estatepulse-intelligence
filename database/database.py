import sqlite3

connection = sqlite3.connect("database/estatepulse.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS property_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id TEXT,
    title TEXT,
    price TEXT,
    location TEXT,
    bedrooms TEXT,
    bathrooms TEXT,
    size TEXT,
    property_type TEXT,
    availability TEXT,
    url TEXT,
    date_scraped TEXT
)
""")

connection.commit()

print("Database setup completed")

connection.close()