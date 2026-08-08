import sqlite3
import os

from analysis.history_analysis import get_latest_properties


# =====================================================
# DATABASE PATH
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "estatepulse.db"
)


# =====================================================
# DETECT CHANGES FOR ONE PROPERTY
# =====================================================

def detect_property_changes(property_id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            property_id,
            title,
            price,
            availability,
            date_scraped
        FROM property_snapshots
        WHERE property_id = ?
        ORDER BY date_scraped ASC
    """, (property_id,))

    history = cursor.fetchall()

    conn.close()

    changes = []

    for i in range(1, len(history)):

        previous = history[i - 1]
        current = history[i]

        # =============================================
        # PRICE CHANGE
        # =============================================

        if previous[2] != current[2]:

            changes.append({
                "property_id": current[0],
                "title": current[1],
                "change": "Price changed",
                "old_price": previous[2],
                "new_price": current[2],
                "old_status": previous[3],
                "new_status": current[3],
                "date": current[4]
            })

        # =============================================
        # AVAILABILITY CHANGE
        # =============================================

        if previous[3] != current[3]:

            changes.append({
                "property_id": current[0],
                "title": current[1],
                "change": "Availability changed",
                "old_price": previous[2],
                "new_price": current[2],
                "old_status": previous[3],
                "new_status": current[3],
                "date": current[4]
            })

    return changes


# =====================================================
# DETECT ALL MARKET CHANGES
# =====================================================

def detect_all_changes():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT property_id
        FROM property_snapshots
    """)

    property_ids = cursor.fetchall()

    conn.close()

    all_changes = []

    for row in property_ids:

        property_id = row[0]

        changes = detect_property_changes(
            property_id
        )

        all_changes.extend(changes)

    return all_changes


# =====================================================
# COUNT NEW LISTINGS
# =====================================================

def count_new_listings():

    latest = get_latest_properties()

    return len(latest)