import sqlite3
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "estatepulse.db"
)


def save_snapshot(property_data):

    connection = sqlite3.connect(
        DB_PATH,
        timeout=10
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO property_snapshots (
            property_id,
            title,
            price,
            location,
            bedroom,
            bathroom,
            size,
            apartment_type,
            availability,
            url,
            date_scraped
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            property_data["property_id"],
            property_data["title"],
            property_data["price"],
            property_data["location"],
            property_data["bedroom"],
            property_data["bathroom"],
            property_data["size"],
            property_data["apartment_type"],
            property_data["availability"],
            property_data["url"],
            property_data["date_scraped"]
        )
    )

    connection.commit()
    connection.close()


def get_property_history(property_id):

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            property_id,
            title,
            price,
            availability,
            date_scraped
        FROM property_snapshots
        WHERE property_id = ?
        ORDER BY date_scraped DESC
        """,
        (property_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    history = []

    for row in rows:

        history.append(
            {
                "property_id": row[0],
                "title": row[1],
                "price": row[2],
                "availability": row[3],
                "date": row[4]
            }
        )

    return history