import streamlit as st
import pandas as pd

from database.history import get_property_history
from analysis.market_analysis import get_properties


def show_history():

    st.title("🕘 Property History")

    st.caption(
        "Track historical price and availability changes for properties."
    )

    properties = get_properties()

    if not properties:
        st.warning("No property records found.")
        return

    # Create property selection
    property_options = {}

    for property in properties:

        property_id = property[0]
        title = property[1]

        property_options[
            f"{title}"
        ] = property_id

    selected_property = st.selectbox(
        "🏠 Select Property",
        list(property_options.keys())
    )

    selected_property_id = property_options[selected_property]

    # Get history
    history = get_property_history(
        selected_property_id
    )

    if not history:

        st.info(
            "No historical records found for this property."
        )

        return

    history_df = pd.DataFrame(history)

    st.subheader("📋 Historical Records")

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )
    