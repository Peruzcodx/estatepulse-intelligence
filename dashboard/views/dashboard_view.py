import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from analysis.market_analysis import (
    get_properties,
    analyze_prices,
    analyze_areas,
    analyze_property_types,
    analyze_availability,
    analyze_price_segments,
    analyze_market_value_by_area,
    extract_area,
)

def show_dashboard(selected_location):

    properties = get_properties()

    if selected_location != "All":

        properties = [
            item for item in properties
            if extract_area(item[3]) == selected_location
        ]
    if len(properties) == 0:

        st.warning(
            "No properties found for this location."
        )

        return

    average, highest, lowest = analyze_prices(properties)

    st.title("🏠 EstatePulse Intelligence Dashboard")
    
    if selected_location =="All":
        st.info(" showing nationwide analysis")
    else:
        st.info(f" Showing {selected_location} market  analysis")
    st.write(f"Active Market Records: {len(properties)}")

    st.caption(
        "Nigeria Real Estate Market Analytics Platform"
    )
    nigeria_time = datetime.now(ZoneInfo("Africa/Lagos"))

    st.caption(
        f"🕒 Last Updated: {nigeria_time.strftime('%d %B %Y, %I:%M %p')}"
    )


    st.divider()


    st.subheader("📊 Market Overview")


    col1, col2, col3 = st.columns(3)


    with col1:
        st.metric(
            "🏘 Total Properties",
            len(properties)
        )


    with col2:
        st.metric(
            "💵 Average Price",
            f"₦{average:,.0f}"
        )


    with col3:
        st.metric(
            "🔥 Highest Price",
            f"₦{highest:,.0f}"
        )
    st.divider()

    st.subheader("📈 Real Estate Market Analytics")


    property_types = analyze_property_types(properties)

    labels = []
    values = []

    for property_type, count in property_types:
        labels.append(property_type)
        values.append(count)

    locations = analyze_areas(properties)

    top_locations = locations[:5]

    location_names = []
    location_counts = []

    for location, count in top_locations:
        location_names.append(location)
        location_counts.append(count)
    col1, col2 = st.columns(2)

    availability = analyze_availability(properties)

    availability_labels = []
    availability_values = []

    for status, count in availability:
        availability_labels.append(status)
        availability_values.append(count)

    with col1:

        st.subheader("🏠 Property Distribution by Types")

        property_chart = px.pie(
            names=labels,
            values=values
        )
        property_chart.update_layout(
            height=400
        )

        st.plotly_chart(
            property_chart,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )


    with col2:

        st.subheader("📍 Top Locations by Active Listings")

        location_chart = px.bar(
        x=location_counts,
        y=location_names,
        orientation="h"
        )

        location_chart.update_layout(
        height=400
        )
        st.plotly_chart(
            location_chart,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "scrollZoom": False,
                "staticPlot": True
            }
        )
    st.divider()
    price_segments = analyze_price_segments(properties)

    segment_labels = []
    segment_values = []

    for segment, count in price_segments:
        segment_labels.append(segment)
        segment_values.append(count)

    market_values = analyze_market_value_by_area(properties)

    top_market_values = market_values[:10]

    area_names = []
    area_values = []

    for area, value in top_market_values:
        area_names.append(area)
        area_values.append(value)
    
    col3, col4 = st.columns(2)
    with col3:

        st.subheader("📌 Inventory Availability")

        availability_chart = px.pie(
            names=availability_labels,
            values=availability_values,
            hole=0.55
        )

        availability_chart.update_layout(
            height=400
        )

        st.plotly_chart(
            availability_chart,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "scrollZoom": False,
                "staticPlot": True
            }
        )
    with col4:

        st.subheader("💰 Market Price Segmentation")

        segment_chart = px.pie(
            names=segment_labels,
            values=segment_values,
            hole=0.55
        )

        segment_chart.update_layout(
            height=400
        )

        st.plotly_chart(
            segment_chart,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "scrollZoom": False,
                "staticPlot": True
            }
        )

    st.divider()

    st.subheader("💎 Total Market Value Concentration by Area ")


    market_value_chart = px.bar(
        x=area_values,
        y=area_names,
        orientation="h"
    )


    market_value_chart.update_layout(
        height=500,
        yaxis={
            "categoryorder": "total ascending"
        }
    )


    st.plotly_chart(
        market_value_chart,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "scrollZoom": False,
            "staticPlot": True
        }
    )
    st.divider()

    st.subheader("🧠 Market Insights")
   
    most_common_type = property_types[0][0]


    # Most active location

    top_location = locations[0][0]


    # Largest market value area

    highest_value_area = market_values[0][0]


    # Dominant price segment

    dominant_segment = price_segments[0][0]
    insight_col1, insight_col2 = st.columns(2)


    with insight_col1:

        st.info(
            f"""
            🏠 **Property Demand**

            {most_common_type} is currently the most common property type in the market.
            """
        )


        st.info(
            f"""
            📍 **Location Activity**

            {top_location} has the highest number of active listings.
            """
        )


    with insight_col2:

        st.info(
            f"""
            💰 **Market Segment**

            {dominant_segment} properties represent the dominant price category.
            """
        )


        st.info(
            f"""
            💎 **Market Value Concentration**

            {highest_value_area} represents the highest total property value concentration.
            """
        )
        st.divider()


    st.divider()

    st.subheader("🗂 Property Explorer")


    property_data = []


    for item in properties:

        property_data.append(
            {
                "Title": item[1],
                "Price": item[2],
                "Location": item[3],
                "Bedrooms": item[4],
                "Bathrooms": item[5],
                "Size": item[6],
                "Type": item[7],
                "Status": item[8]
            }
        )


    df = pd.DataFrame(property_data)

    filter_col1, filter_col2, filter_col3 = st.columns(3)


    with filter_col1:

        selected_type = st.selectbox(
            "🏠 Property Type",
            ["All"] + sorted(df["Type"].unique()),
            key=f"property_type_{selected_location}"
        )


    with filter_col2:

        search_property = st.text_input(
            "🔍 Search Property",
            key=f"property_search_{selected_location}"
        )


    with filter_col3:

        # Convert prices to numbers FIRST, then take min/max.
        # Taking min()/max() on the raw strings sorts them
        # lexicographically (e.g. "122000000" < "95000000"
        # because '1' < '9'), which produced a wrong, narrow
        # price range and broke the "All" filter.
        numeric_prices = (
            df["Price"]
            .str.replace("₦", "", regex=False)
            .str.replace(",", "", regex=False)
            .astype(int)
        )

        minimum_price = int(numeric_prices.min())
        maximum_price = int(numeric_prices.max())


        if minimum_price == maximum_price:

            selected_price = (
                minimum_price,
                maximum_price
            )

            st.write(
                f"💰 Price: ₦{minimum_price:,.0f}"
            )

        else:

            selected_price = st.slider(
                "💰 Price Range",
                min_value=minimum_price,
                max_value=maximum_price,
                value=(minimum_price, maximum_price),
                step=1_000_000,
                format="₦%d",
                key=f"property_price_range_{selected_location}"
            )
        filtered_df = df.copy()


    # Property Type Filter

    if selected_type != "All":

        filtered_df = filtered_df[
            filtered_df["Type"] == selected_type
        ]


    # Search Filter

    if search_property:

        filtered_df = filtered_df[
            filtered_df["Title"].str.contains(
                search_property,
                case=False
            )
        ]


    # Price Filter

    filtered_df["Numeric Price"] = (
        filtered_df["Price"]
        .str.replace("₦", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(int)
    )


    filtered_df = filtered_df[
        (filtered_df["Numeric Price"] >= selected_price[0])
        &
        (filtered_df["Numeric Price"] <= selected_price[1])
    ]


    filtered_df = filtered_df.drop(
        columns=["Numeric Price"]
    )

    st.success(
        f"Showing {len(filtered_df)} of {len(df)} properties"
    )


    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        height=450
    )