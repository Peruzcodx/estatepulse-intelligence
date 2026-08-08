
import streamlit as st
import sqlite3
import os
import pandas as pd
import plotly.express as px


# =====================================================
# DATABASE
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "estatepulse.db"
)


# =====================================================
# LOAD MARKET HISTORY
# =====================================================

def get_market_history():

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            date_scraped,
            price,
            property_id
        FROM property_snapshots
        WHERE property_id IS NOT NULL
        ORDER BY date_scraped
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# =====================================================
# MARKET TRENDS PAGE
# =====================================================

def show_market():

    st.title("📈 Market Trends")

    st.caption(
        "Historical analysis of the Nigerian real estate market"
    )

    df = get_market_history()

    if df.empty:

        st.warning(
            "No historical market data is available yet."
        )

        return


    # =================================================
    # CLEAN DATA
    # =================================================

    df["date_scraped"] = pd.to_datetime(
        df["date_scraped"],
        format="mixed",
        errors="coerce"
    )

    df["price_numeric"] = (
        df["price"]
        .str.replace("₦", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    df["date"] = df["date_scraped"].dt.date


    # Remove invalid dates if any exist
    df = df.dropna(subset=["date_scraped"])


    # =================================================
    # DAILY MARKET SUMMARY
    # =================================================

    daily_market = (
        df.groupby("date")
        .agg(
            average_price=("price_numeric", "mean"),
            highest_price=("price_numeric", "max"),
            lowest_price=("price_numeric", "min"),
            snapshots=("property_id", "count"),
            unique_properties=("property_id", "nunique")
        )
        .reset_index()
    )


    if daily_market.empty:

        st.warning(
            "Not enough historical data to generate market trends."
        )

        return


    # =================================================
    # PAGE SUMMARY
    # =================================================

    first_average = daily_market.iloc[0]["average_price"]

    latest_average = daily_market.iloc[-1]["average_price"]


    if first_average > 0:

        price_change = (
            (latest_average - first_average)
            / first_average
        ) * 100

    else:

        price_change = 0


    # =================================================
    # KPI SECTION
    # =================================================

    st.subheader("📊 Market Trend Overview")

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Historical Snapshots",
            len(df)
        )


    with col2:

        st.metric(
            "Tracked Properties",
            df["property_id"].nunique()
        )


    with col3:

        st.metric(
            "Latest Avg. Price",
            f"₦{latest_average:,.0f}"
        )


    with col4:

        st.metric(
            "Price Change",
            f"{price_change:+.1f}%"
        )


    st.divider()


    # =================================================
    # AVERAGE PRICE TREND
    # =================================================

    st.subheader("💰 Average Property Price Trend")


    price_chart = px.line(
        daily_market,
        x="date",
        y="average_price",
        markers=True,
        labels={
            "date": "Date",
            "average_price": "Average Price"
        }
    )


    price_chart.update_traces(
        hovertemplate=
        "Date: %{x}<br>"
        "Average Price: ₦%{y:,.0f}"
        "<extra></extra>"
    )


    price_chart.update_layout(
        height=450,
        template="plotly_white"
    )


    st.plotly_chart(
        price_chart,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "scrollZoom": False,
            "staticPlot": True
        },
        key="market_price_trend"
    )


    st.divider()


    # =================================================
    # MARKET ACTIVITY
    # =================================================

    st.subheader("🏘 Market Activity Over Time")


    activity_chart = px.bar(
        daily_market,
        x="date",
        y="snapshots",
        labels={
            "date": "Date",
            "snapshots": "Recorded Snapshots"
        }
    )


    activity_chart.update_layout(
        height=400,
        template="plotly_white"
    )


    st.plotly_chart(
        activity_chart,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "scrollZoom": False,
            "staticPlot": True
        },
        key="market_activity_trend"
    )


    st.divider()


    # =================================================
    # MARKET RANGE
    # =================================================

    st.subheader("📊 Daily Market Price Range")


    range_chart = px.line(
        daily_market,
        x="date",
        y=[
            "highest_price",
            "average_price",
            "lowest_price"
        ],
        labels={
            "date": "Date",
            "value": "Price",
            "variable": "Price Level"
        }
    )


    range_chart.update_layout(
        height=450,
        template="plotly_white"
    )


    # IMPORTANT:
    # Plot range_chart here, NOT activity_chart.

    st.plotly_chart(
        range_chart,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "scrollZoom": False,
            "staticPlot": True
        },
        key="daily_market_price_range"
    )


    st.divider()


    # =================================================
    # MARKET INSIGHTS
    # =================================================

    st.subheader("🧠 Trend Insights")


    if price_change > 0:

        trend_message = (
            f"Average property prices increased by "
            f"**{price_change:.1f}%** across the available "
            f"historical period."
        )

    elif price_change < 0:

        trend_message = (
            f"Average property prices decreased by "
            f"**{abs(price_change):.1f}%** across the available "
            f"historical period."
        )

    else:

        trend_message = (
            "Average property prices remained relatively "
            "stable across the available historical period."
        )


    col1, col2 = st.columns(2)


    with col1:

        st.info(
            f"""
            💰 **Price Movement**

            {trend_message}
            """
        )


    with col2:

        st.info(
            f"""
            📊 **Historical Coverage**

            EstatePulse currently contains
            **{len(df):,} historical snapshots**
            covering **{df["property_id"].nunique()} unique properties**.
            """
        )


    # =================================================
    # DAILY DATA TABLE
    # =================================================

    with st.expander(
        "📋 View Historical Market Data"
    ):

        display_df = daily_market.copy()


        display_df["average_price"] = (
            display_df["average_price"]
            .map(lambda x: f"₦{x:,.0f}")
        )


        display_df["highest_price"] = (
            display_df["highest_price"]
            .map(lambda x: f"₦{x:,.0f}")
        )


        display_df["lowest_price"] = (
            display_df["lowest_price"]
            .map(lambda x: f"₦{x:,.0f}")
        )


        display_df.columns = [
            "Date",
            "Average Price",
            "Highest Price",
            "Lowest Price",
            "Snapshots",
            "Unique Properties"
        ]


        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
