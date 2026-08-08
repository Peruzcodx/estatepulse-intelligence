import sqlite3
import os

from analysis.data_cleaning import clean_locations


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(
    BASE_DIR,
    "estatepulse.db"
)


connection = sqlite3.connect(DB_PATH)

cursor = connection.cursor()


cursor.execute(
    "SELECT id, location FROM property_snapshots"
)

properties = cursor.fetchall()


for property in properties:

    property_id = property[0]

    location = property[1]

    area = clean_locations(location)


    cursor.execute(
        """
        UPDATE property_snapshots
        SET area = ?
        WHERE id = ?
        """,
        (area, property_id)
    )


connection.commit()

connection.close()


print("Area data updated successfully")