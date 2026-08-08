import sqlite3

connection = sqlite3.connect("database/estatepulse.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM property_snapshots")

properties= cursor.fetchall()

for property in properties:
    print(property)
    connection.close()

def clear_database():
    connection = sqlite3.connect("database/estatepulse.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM property_snapshots")

    connection.commit()
    connection.close()