import streamlit as st
import plotly.express as px
import pandas as pd
import os 
from datetime import datetime

from analysis.market_analysis import (
    get_properties,
    analyze_prices,
    analyze_property_types,
    analyze_availability,
    analyze_market_value_by_area,
    analyze_price_segments,
    analyze_areas
)
from analysis.history_analysis import (
    get_latest_properties,
    get_property_changes
)

from views.history_view import show_history

from analysis.change_detector import count_new_listings

# =====================================================
# PAGE CONFIG
# =====================================================

logo_path = os.path.join(
    os.path.dirname(__file__),
    "assets",
    "logo.png"
)
st.set_page_config(
    page_title="EstatePulse Intelligence",
    page_icon=logo_path,
    layout="wide",
    initial_sidebar_state="expanded"
)
if "page" not in st.session_state:
    st.session_state.page = "dashboard"
# =====================================================
# SIDEBAR BRANDING
# =====================================================

logo_path = os.path.join(
    os.path.dirname(__file__),
    "assets",
    "logo.png"
)


st.markdown("""
<style>

section[data-testid="stSidebar"] {
    background-color:#1a1a2e;
}

</style>
""", unsafe_allow_html=True)


# THEN LOAD DATA BELOW


# =====================================================
# LOAD DATA
# =====================================================

properties = get_properties()

average, highest, lowest = analyze_prices(properties)

property_types = analyze_property_types(properties)

locations = analyze_areas(properties)

availability = analyze_availability(properties)

market_values = analyze_market_value_by_area(properties)
price_segments = analyze_price_segments(properties)
latest_properties = get_latest_properties()

changes = get_property_changes()
new_listings = count_new_listings()

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    logo_path = os.path.join(
        os.path.dirname(__file__),
        "assets",
        "logo.png"
    )
    if os.path.exists(logo_path):
        st.image(logo_path, width=180)
    else:
        st.markdown("## 🏠 EstatePulse")

    st.title("EstatePulse")
    st.success("Market Intelligence Platform")
    st.divider()
    st.subheader("🔎 Market Filters")

    

    available_locations = ["All"]

    for location, count in locations:
        available_locations.append(location)


    selected_location = st.selectbox(
        "Select Location",
        available_locations
    )

    st.divider()
# =====================================================
# NAVIGATION
# =====================================================

    st.subheader("Navigation")

    if st.button("🏠 Dashboard"):
        st.session_state.page = "dashboard"
    
    if st.button("📜 Property History"):
        st.session_state.page = "history"

    if st.button("🔍 Change Detector"):
        st.session_state.page = "changes"
    
    if st.button("📈 Market Trends"):
        st.session_state.page = "market"

    if st.button("📑 Reports"):
        st.session_state.page = "reports"
    st.write("Current page:", st.session_state.get("page"))
    st.divider()

    st.subheader("Database")
    st.write(f"Properties : {len(properties)}")
    st.success("🟢 Connected")
    st.divider()

    st.subheader("System")
    st.write("Version : 1.0")
    st.write("Database : SQLite")
    st.write("Dashboard : Streamlit")
    st.write("Charts : Plotly")
    st.divider()

    st.info("Built using Python, SQLite, Plotly and Streamlit.")

    if st.button("🔄 Refresh Dashboard"):
        st.rerun()


# =====================================================
# PAGE ROUTER
# =====================================================




if st.session_state.page == "dashboard":

    from views.dashboard_view import show_dashboard
    show_dashboard(selected_location)


elif st.session_state.page == "history":

    from views.history_view import show_history
    show_history()


elif st.session_state.page == "changes":

    from views.change_view import show_changes
    show_changes()


elif st.session_state.page == "market":

    from views.market_view import show_market
    show_market()


elif st.session_state.page == "reports":

    from views.reports_view import show_reports
    show_reports()


# # =====================================================
# # HEADER
# # =====================================================



# st.title("🏠 EstatePulse Intelligence Dashboard")


# st.write(f"Records : {len(properties)}")
# st.caption(
#     "Nigeria Real Estate Market Analytics Platform"
# )

# st.caption(
#     f"🕒 Last Updated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}"
# )

# st.divider()


# # =====================================================
# # MARKET CHANGES
# # =====================================================
# st.subheader("📈 Market Changes")

# col1, col2, col3 = st.columns(3)

# with col1:
#     st.metric(
#         "Current Active Listings",
#         len(latest_properties)
#     )

# with col2:
#     st.metric(
#         "Historical Records",
#         len(changes)
#     )
# with col3:
#     st.metric(
#         "🆕 New Listings",
#         new_listings
#     )
# # =====================================================
# # MARKET SUMMARY
# # =====================================================

# st.info(
#     f"""
# ### 📌 EstatePulse Market Summary

# - Total Listings: **{len(properties)}**
# - Average Market Price: **₦{average:,.0f}**
# - Highest Listing: **₦{highest:,.0f}**
# - Lowest Listing: **₦{lowest:,.0f}**
# - Most Popular Property Type: **{property_types[0][0]}**
# - Top Property Location: **{locations[0][0]}**
# """
# )

# st.divider()


# # =====================================================
# # MARKET INSIGHTS
# # =====================================================

# st.subheader("📈 Market Insights")

# available_count = availability[0][1]

# availability_percentage = (
#     available_count / len(properties)
# ) * 100

# highest_location = locations[0][0]

# highest_location_count = locations[0][1]

# highest_market_area = market_values[0][0]

# highest_market_value = market_values[0][1]

# insight1 = (
#     f"🏘 **{property_types[0][0]}** "
#     f"is currently the most common property type."
# )

# insight2 = (
#     f"📍 **{highest_location}** has the highest number "
#     f"of listings ({highest_location_count})."
# )

# insight3 = (
#     f"💰 **{highest_market_area}** has the highest "
#     f"combined market value "
#     f"(₦{highest_market_value:,.0f})."
# )

# insight4 = (
#     f"✅ {availability_percentage:.1f}% "
#     "of listed properties are currently available."
# )

# insight5 = (
#     f"📊 Average property listing price is "
#     f"₦{average:,.0f}."
# )

# st.success(insight1)

# st.success(insight2)

# st.success(insight3)

# st.success(insight4)

# st.success(insight5)

# st.divider()

# #Market Summary

# st.subheader("📝 Market Summary")

# st.info(
#     f"""
# EstatePulse currently tracks **{len(properties)}** verified properties.

# The average property price is **₦{average:,.0f}**, while the highest listing is **₦{highest:,.0f}**.

# **{property_types[0][0]}** remains the most common property type.

# **{locations[0][0]}** currently has the highest number of listings.

# The area with the largest combined market value is **{market_values[0][0]}**.

# Approximately **{availability_percentage:.1f}%** of all properties are currently available for sale or rent.
# """
# )



# # =====================================================
# # CHARTS
# # =====================================================



# st.subheader("📈 Price Segment Analysis")

# segment_names = [
#     segment
#     for segment, count in price_segments
# ]

# segment_counts = [
#     count
#     for segment, count in price_segments
# ]

# fig = px.bar(
#     x=segment_counts,
#     y=segment_names,
#     text=segment_counts,
#     labels={
#         "x": "Market Segment",
#         "y": "Number of Properties"
#     },
#     title="Property Market Segments"
# )

# fig.update_traces(
#     textposition="outside"
# )

# fig.update_layout(
#     title_x=0.5,
#     height=400,
#     template="plotly_white"
# )
# st.plotly_chart(
#     fig,
#     use_container_width=True,
#     config={
#         "displayModeBar": False,
#         "scrollZoom": False,
#         "staticPlot": True
#     }
# )
# col1, col2 = st.columns(2)
# # =====================================================
# # PROPERTY DISTRIBUTION
# # =====================================================

# with col1:

#     type_names = [name for name, count in property_types]
#     type_counts = [count for name, count in property_types]

#     fig = px.bar(
#         x=type_names,
#         y=type_counts,
#         text=type_counts,
#         labels={
#             "x": "Property Type",
#             "y": "Number of Listings"
#         },
#         title="🏘 Property Distribution"
#     )

#     fig.update_traces(
#         textposition="outside"
#     )

#     fig.update_layout(
#         title_x=0.5,
#         height=420,
#         template="plotly_white"
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True,
#         config={
#             "displayModeBar": False,
#             "scrollZoom": False,
#             "staticPlot": True
#         }
#     )

# # =====================================================
# # PROPERTY AVAILABILITY
# # =====================================================

# with col2:

#     availability_names = [
#         status
#         for status, count in availability
#     ]

#     availability_counts = [
#         count
#         for status, count in availability
#     ]

#     fig = px.pie(
#         names=availability_names,
#         values=availability_counts,
#         title="✅ Property Availability",
#         hole=0.4
#     )

#     fig.update_traces(
#         textposition="outside"
#     )

#     fig.update_layout(
#         title_x=0.5,
#         height=420,
#         template="plotly_white"
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True,
#         config={
#             "displayModeBar": False,
#             "scrollZoom": False,
#             "staticPlot": True
#         }
#     )

# # =====================================================
# # SECOND ROW
# # =====================================================

# col3, col4 = st.columns(2)

# # =====================================================
# # TOP LOCATIONS
# # =====================================================

# with col3:

#     location_names = [
#         location
#         for location, count in locations
#     ]

#     location_counts = [
#         count
#         for location, count in locations
#     ]

#     fig = px.bar(
#         x=location_names,
#         y=location_counts,
#         text=location_counts,
#         labels={
#             "x": "Area",
#             "y": "Listings"
#         },
#         title="📍 Top Locations"
#     )

#     fig.update_traces(
#         textposition="outside"
#     )

#     fig.update_layout(
#         title_x=0.5,
#         height=420,
#         template="plotly_white"
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True,
#         config={
#             "displayModeBar": False,
#             "scrollZoom": False,
#             "staticPlot": True
#         }
#     )

# # =====================================================
# # MARKET VALUE BY AREA
# # =====================================================

# with col4:

#     area_names = [
#         area
#         for area, value in market_values
#     ]

#     area_values = [
#         value
#         for area, value in market_values
#     ]

#     fig = px.bar(
#         x=area_names,
#         y=area_values,
#         text=[
#             f"₦{value/1_000_000:.0f}M"
#             for value in area_values
#         ],
#         labels={
#             "x": "Area",
#             "y": "Total Market Value"
#         },
#         title="💰 Market Value by Area"
#     )

#     fig.update_traces(
#         textposition="outside"
#     )

#     fig.update_layout(
#         title_x=0.5,
#         height=420,
#         template="plotly_white"
#     )

#     st.plotly_chart(
#     fig,
#     use_container_width=True,
#     config={
#         "displayModeBar": False,
#         "scrollZoom": False,
#         "staticPlot": True
#     }
# )

# st.divider()

# # =====================================================
# # PROPERTY EXPLORER
# # =====================================================

# st.subheader("🗂 Property Explorer")

# property_data = []

# for property in properties:

#     property_data.append(
#         {
#             "Title": property[1],
#             "Price": property[2],
#             "Location": property[3],
#             "Bedrooms": property[4],
#             "Bathrooms": property[5],
#             "Type": property[7],
#             "Status": property[8]
#         }
#     )

# df = pd.DataFrame(property_data)

# # -----------------------------------------------------
# # CREATE NUMERIC PRICE
# # -----------------------------------------------------

# df["Numeric Price"] = (
#     df["Price"]
#       .str.replace("₦", "", regex=False)
#       .str.replace(",", "", regex=False)
#       .astype(int)
# )

# st.markdown("### 🔍 Filter Properties")

# filter1, filter2, filter3 = st.columns(3)

# with filter1:

#     selected_location = st.selectbox(
#         "📍 Location",
#         ["All"] + sorted(df["Location"].unique())
#     )

# with filter2:

#     selected_type = st.selectbox(
#         "🏠 Property Type",
#         ["All"] + sorted(df["Type"].unique())
#     )

# with filter3:

#     search = st.text_input(
#         "🔎 Search Title"
#     )

# minimum = int(df["Numeric Price"].min())

# maximum = int(df["Numeric Price"].max())

# price_range = st.slider(
#     "💰 Price Range",
#     minimum,
#     maximum,
#     (minimum, maximum),
#     step=1000000,
#     format="₦%d"
# )

# # -----------------------------------------------------
# # APPLY FILTERS
# # -----------------------------------------------------

# filtered_df = df.copy()

# if selected_location != "All":

#     filtered_df = filtered_df[
#         filtered_df["Location"] == selected_location
#     ]

# if selected_type != "All":

#     filtered_df = filtered_df[
#         filtered_df["Type"] == selected_type
#     ]

# if search:

#     filtered_df = filtered_df[
#         filtered_df["Title"].str.contains(
#             search,
#             case=False
#         )
#     ]

# filtered_df = filtered_df[
#     (filtered_df["Numeric Price"] >= price_range[0]) &
#     (filtered_df["Numeric Price"] <= price_range[1])
# ]

# filtered_df = filtered_df.drop(
#     columns=["Numeric Price"]
# )

# st.success(
#     f"Showing {len(filtered_df)} of {len(df)} properties"
# )


# st.download_button(
#     label="📥 Download Filtered Data",
#     data=filtered_df.to_csv(index=False).encode("utf-8"),
#     file_name="estatepulse_filtered_properties.csv",
#     mime="text/csv"
# )
# # =====================================================
# # PROPERTY TABLE
# # =====================================================

# with st.expander(
#     "📋 View Property Database",
#     expanded=True
# ):

#     st.dataframe(
#         filtered_df,
#         use_container_width=True,
#         hide_index=True,
#         height=450
#     )


# # =====================================================
# # QUICK STATISTICS
# # =====================================================

# st.divider()

# st.subheader("📌 Quick Statistics")

# col1, col2, col3 = st.columns(3)

# with col1:

#     st.info(
#         f"🏘 Listings Displayed\n\n{len(filtered_df)}"
#     )

# with col2:

#     st.info(
#         f"📍 Locations\n\n{filtered_df['Location'].nunique()}"
#     )

# with col3:

#     st.info(
#         f"🏠 Property Types\n\n{filtered_df['Type'].nunique()}"
#     )

# # =====================================================
# # FOOTER
# # =====================================================

# st.divider()


# st.divider()

# st.subheader("🏆 Top 5 Most Expensive Properties")

# top_properties = (
#     filtered_df.copy()
# )

# top_properties["Price Value"] = (
#     top_properties["Price"]
#     .str.replace("₦", "", regex=False)
#     .str.replace(",", "", regex=False)
#     .astype(int)
# )

# top_properties = top_properties.sort_values(
#     by="Price Value",
#     ascending=False
# )

# top_properties = top_properties.drop(
#     columns=["Price Value"]
# )

# st.dataframe(
#     top_properties.head(5),
#     use_container_width=True,
#     hide_index=True
# )

# st.caption(
#     "EstatePulse Intelligence Dashboard v1.0 | Python • SQLite • Plotly • Streamlit"
# )
