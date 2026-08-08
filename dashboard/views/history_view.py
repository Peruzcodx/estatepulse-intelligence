import streamlit as st
import sqlite3
import os
import pandas as pd
import plotly.express as px

from database.history import get_property_history


# =====================================================
# DATABASE PATH
# =====================================================

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


# =====================================================
# PROPERTY HISTORY PAGE
# =====================================================

def show_history():

    st.title("📜 Property History")

    st.caption(
        "Track historical price and availability changes for properties."
    )

    st.divider()

    # =================================================
    # GET ALL PROPERTIES
    # =================================================

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
        st.info("No property history records found.")
        return

    # =================================================
    # PROPERTY SELECTOR
    # =================================================

    property_options = {
        title: property_id
        for property_id, title in properties
    }

    selected_title = st.selectbox(
        "🏠 Select Property",
        list(property_options.keys())
    )

    selected_property_id = property_options[selected_title]

    # =================================================
    # GET HISTORY
    # =================================================

    history = get_property_history(
        selected_property_id
    )

    if not history:
        st.warning(
            "No historical records found for this property."
        )
        return

    # =================================================
    # CONVERT TO DATAFRAME
    # =================================================

    df = pd.DataFrame(history)

    # Convert price from strings like ₦290,000,000
    # into numbers

    df["price_value"] = (
        df["price"]
        .astype(str)
        .str.replace("₦", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace("M", "", regex=False)
        .str.strip()
    )

    def convert_price(value):

        try:
            if value == "":
                return 0

            return float(value)

        except:
            return 0

    df["price_value"] = df["price_value"].apply(
        convert_price
    )

    # =================================================
    # SORT HISTORY
    # =================================================

    df = df.sort_values(
        by="date"
    )

    # =================================================
    # CURRENT / PREVIOUS PRICE
    # =================================================

    current_price = df.iloc[-1]["price_value"]

    if len(df) > 1:

        previous_price = df.iloc[-2]["price_value"]

    else:

        previous_price = current_price

    price_change = current_price - previous_price

    if previous_price != 0:

        percentage_change = (
            price_change / previous_price
        ) * 100

    else:

        percentage_change = 0

    current_status = df.iloc[-1]["availability"]

    # =================================================
    # PROPERTY SUMMARY
    # =================================================

    st.subheader(selected_title)

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Current Price",
            f"₦{current_price:,.0f}"
        )

    with col2:

        if len(df) > 1:

            st.metric(
                "Previous Price",
                f"₦{previous_price:,.0f}"
            )

        else:

            st.metric(
                "Previous Price",
                "N/A"
            )

    with col3:

        st.metric(
            "Price Change",
            f"₦{price_change:,.0f}",
            delta=f"{percentage_change:.2f}%"
        )

    with col4:

        st.metric(
            "Historical Records",
            len(df)
        )

    st.write(
        f"**Current Status:** {current_status}"
    )

    st.divider()

    # =================================================
    # PRICE HISTORY CHART
    # =================================================

    st.subheader("📈 Price History")

    if len(df) > 1:

        fig = px.line(
            df,
            x="date",
            y="price_value",
            markers=True,
            labels={
                "date": "Date",
                "price_value": "Price (₦)"
            },
            title="Property Price Movement"
        )

        fig.update_layout(
            height=420,
            template="plotly_white"
        )

        st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "scrollZoom": False,
            "staticPlot": True
            }
        )
        
    else:

        st.info(
            "A price history chart will appear after "
            "multiple snapshots are recorded."
        )

    # =================================================
    # PRICE MOVEMENT
    # =================================================

    st.subheader("🔄 Price Movement")

    if len(df) <= 1:

        st.info(
            "This property has only one recorded snapshot. "
            "No historical price change can be calculated yet."
        )

    elif price_change > 0:

        st.warning(
            f"📈 Price increased by "
            f"₦{price_change:,.0f} "
            f"({percentage_change:.2f}%)."
        )

    elif price_change < 0:

        st.success(
            f"📉 Price decreased by "
            f"₦{abs(price_change):,.0f} "
            f"({abs(percentage_change):.2f}%)."
        )

    else:

        st.info(
            "➡️ No price change detected between "
            "the latest two snapshots."
        )

    # =================================================
    # HISTORICAL RECORDS TABLE
    # =================================================

    st.divider()

    st.subheader("📊 Historical Records")

    display_df = df[
        [
            "property_id",
            "title",
            "price",
            "availability",
            "date"
        ]
    ].copy()

    display_df.columns = [
        "Property ID",
        "Title",
        "Price",
        "Availability",
        "Date"
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    