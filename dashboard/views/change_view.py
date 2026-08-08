import streamlit as st
import sqlite3
import os

from analysis.change_detector import detect_property_changes
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "estatepulse.db"
)


def show_changes():

    st.title("🔍 Change Detector")

    st.caption(
        "Detect price and availability changes across property listings."
    )

    st.divider()

    # ---------------------------------------------
    # GET ALL PROPERTIES
    # ---------------------------------------------

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT property_id, title
        FROM property_snapshots
        ORDER BY title
    """)

    properties = cursor.fetchall()

    conn.close()

    if not properties:
        st.info("No property records found.")
        return

    # ---------------------------------------------
    # PROPERTY SELECTOR
    # ---------------------------------------------

    property_options = {
        title: property_id
        for property_id, title in properties
    }

    selected_title = st.selectbox(
        "🏠 Select Property",
        list(property_options.keys())
    )

    selected_property_id = property_options[selected_title]

    # ---------------------------------------------
    # DETECT CHANGES
    # ---------------------------------------------

    changes = detect_property_changes(
        selected_property_id
    )

    st.divider()

    if not changes:

        st.success(
            "✅ No price or availability changes detected."
        )

        return

    # ---------------------------------------------
    # SUMMARY
    # ---------------------------------------------

    st.subheader("📊 Detected Changes")

    col1, col2 = st.columns(2)

    price_changes = [
        change
        for change in changes
        if change["change"] == "Price changed"
    ]

    availability_changes = [
        change
        for change in changes
        if change["change"] == "Availability changed"
    ]

    with col1:
        st.metric(
            "💰 Price Changes",
            len(price_changes)
        )

    with col2:
        st.metric(
            "🏷 Availability Changes",
            len(availability_changes)
        )

    st.divider()

    # ---------------------------------------------
    # DISPLAY CHANGES
    # ---------------------------------------------

    for change in changes:

        if change["change"] == "Price changed":

            st.warning(
                f"""
                💰 **Price Changed**

                Previous Price: **{change["old_price"]}**

                New Price: **{change["new_price"]}**

                Date: **{change["date"]}**
                """
            )

        elif change["change"] == "Availability changed":

            st.info(
                f"""
                🏷 **Availability Changed**

                Previous Status: **{change["old_status"]}**

                New Status: **{change["new_status"]}**

                Date: **{change["date"]}**
                """
            )