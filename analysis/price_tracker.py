import sqlite3


def get_price_history(property_id):

    connection = sqlite3.connect(
        "database/estatepulse.db"
    )

    cursor = connection.cursor()

    cursor.execute("""
    SELECT 
        property_id,
        price,
        date_scraped
    FROM property_snapshots
    WHERE property_id = ?
    ORDER BY date_scraped ASC
    """, (property_id,))

    history = cursor.fetchall()
   
    connection.close()

    return history
print(get_price_history("611d454d-a117-4bfd-9187-ac05d2a8b5ad"))