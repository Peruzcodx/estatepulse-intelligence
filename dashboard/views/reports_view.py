import streamlit as st
import sqlite3
import os
import pandas as pd


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
# REPORT PAGE
# =====================================================

def show_reports():

    st.title("📑 Market Reports")

    st.caption(
        "Generate market intelligence reports from the EstatePulse property database."
    )

    st.divider()

    # =================================================
    # LOAD DATA
    # =================================================

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
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
        FROM property_snapshots
        ORDER BY date_scraped DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    if df.empty:
        st.info("No property data available for reporting.")
        return

    # =================================================
    # LATEST PROPERTY RECORDS
    # =================================================

    report_df = df.drop_duplicates(
        subset=["property_id"],
        keep="first"
    ).copy()

    # =================================================
    # NUMERIC PRICE
    # =================================================

    report_df["Price Value"] = (
        report_df["price"]
        .astype(str)
        .str.replace("₦", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(" ", "", regex=False)
    )

    report_df["Price Value"] = pd.to_numeric(
        report_df["Price Value"],
        errors="coerce"
    )

    # =================================================
    # REPORT FILTERS
    # =================================================

    st.subheader("🔎 Report Filters")

    filter1, filter2, filter3 = st.columns(3)

    with filter1:

        locations = sorted(
            report_df["location"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_location = st.selectbox(
            "📍 Location",
            ["All"] + locations,
            key="report_location"
        )

    with filter2:

        property_types_list = sorted(
            report_df["apartment_type"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_type = st.selectbox(
            "🏠 Property Type",
            ["All"] + property_types_list,
            key="report_property_type"
        )

    with filter3:

        availability_list = sorted(
            report_df["availability"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_availability = st.selectbox(
            "🏷 Availability",
            ["All"] + availability_list,
            key="report_availability"
        )

    # =================================================
    # PRICE FILTER
    # =================================================

    minimum_price = int(
        report_df["Price Value"].min()
    )

    maximum_price = int(
        report_df["Price Value"].max()
    )

    price_range = st.slider(
        "💰 Price Range",
        min_value=minimum_price,
        max_value=maximum_price,
        value=(minimum_price, maximum_price),
        step=1000000,
        format="₦%d",
        key="report_price_range"
    )

    # =================================================
    # APPLY FILTERS
    # =================================================

    filtered_df = report_df.copy()

    if selected_location != "All":

        filtered_df = filtered_df[
            filtered_df["location"] == selected_location
        ]

    if selected_type != "All":

        filtered_df = filtered_df[
            filtered_df["apartment_type"] == selected_type
        ]

    if selected_availability != "All":

        filtered_df = filtered_df[
            filtered_df["availability"] == selected_availability
        ]

    filtered_df = filtered_df[
        (filtered_df["Price Value"] >= price_range[0])
        &
        (filtered_df["Price Value"] <= price_range[1])
    ]

    # =================================================
    # FILTER RESULT
    # =================================================

    st.success(
        f"Showing {len(filtered_df)} of "
        f"{len(report_df)} properties"
    )

    # =================================================
    # RESET FILTERS
    # =================================================

    if st.button(
        "🔄 Reset Filters",
        key="reset_report_filters"
    ):

        st.session_state.report_location = "All"
        st.session_state.report_property_type = "All"
        st.session_state.report_availability = "All"
        st.session_state.report_price_range = (
            minimum_price,
            maximum_price
        )

        st.rerun()

    st.divider()

    # =================================================
    # NO RESULTS
    # =================================================

    if filtered_df.empty:

        st.warning(
            "⚠️ No properties match the selected filters."
        )

        return

    # =================================================
    # REPORT SUMMARY
    # =================================================

    st.subheader("📊 Market Summary")

    total_properties = len(filtered_df)

    average_price = filtered_df[
        "Price Value"
    ].mean()

    highest_price = filtered_df[
        "Price Value"
    ].max()

    lowest_price = filtered_df[
        "Price Value"
    ].min()

    total_locations = filtered_df[
        "location"
    ].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🏘 Properties",
            total_properties
        )

    with col2:

        st.metric(
            "💰 Average Price",
            f"₦{average_price:,.0f}"
        )

    with col3:

        st.metric(
            "⬆ Highest Price",
            f"₦{highest_price:,.0f}"
        )

    with col4:

        st.metric(
            "⬇ Lowest Price",
            f"₦{lowest_price:,.0f}"
        )

    st.divider()

    # =================================================
    # AVAILABILITY REPORT
    # =================================================

    st.subheader("🏷 Availability")

    availability = (
        filtered_df["availability"]
        .value_counts()
        .reset_index()
    )

    availability.columns = [
        "Status",
        "Properties"
    ]

    st.dataframe(
        availability,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =================================================
    # PROPERTY TYPE REPORT
    # =================================================

    st.subheader("🏠 Property Types")

    property_types = (
        filtered_df["apartment_type"]
        .value_counts()
        .reset_index()
    )

    property_types.columns = [
        "Property Type",
        "Properties"
    ]

    st.dataframe(
        property_types,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =================================================
    # LOCATION REPORT
    # =================================================

    st.subheader("📍 Location Analysis")

    location_report = (
        filtered_df.groupby("location")
        .agg(
            Properties=("property_id", "count"),
            Average_Price=("Price Value", "mean"),
            Total_Market_Value=("Price Value", "sum")
        )
        .reset_index()
    )

    location_report["Average_Price"] = (
        location_report["Average_Price"]
        .round(0)
    )

    location_report["Total_Market_Value"] = (
        location_report["Total_Market_Value"]
        .round(0)
    )

    location_report = location_report.sort_values(
        by="Properties",
        ascending=False
    )

    st.dataframe(
        location_report,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =================================================
    # PROPERTY REPORT
    # =================================================

    st.subheader("📋 Property Report")

    display_df = filtered_df.drop(
        columns=["Price Value"]
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=450
    )

    st.divider()

    # =================================================
    # DOWNLOAD REPORT
    # =================================================

    st.subheader("📥 Download Report")

    csv_data = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Filtered Property Report",
        data=csv_data,
        file_name="estatepulse_filtered_property_report.csv",
        mime="text/csv",
        key="download_filtered_report"
    )

    # =================================================
    # REPORT FOOTER
    # =================================================

    st.caption(
        f"EstatePulse Intelligence | "
        f"{total_properties} properties | "
        f"{total_locations} locations"
    )