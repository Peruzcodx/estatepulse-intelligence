import sqlite3


def create_tables():

    connection = sqlite3.connect(
        "database/estatepulse.db"
    )

    cursor = connection.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS property_snapshots (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        property_id TEXT,

        title TEXT,

        price TEXT,

        location TEXT,

        bedroom TEXT,

        bathroom TEXT,

        size TEXT,

        apartment_type TEXT,

        availability TEXT,

        url TEXT,

        date_scraped TEXT

    )
    """)


    connection.commit()

    connection.close()


    print("Tables created successfully")