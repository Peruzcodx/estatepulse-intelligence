import matplotlib.pyplot as plt
import os

from analysis.market_analysis import (
    get_properties,
    analyze_availability,
    analyze_property_types,
    analyze_location,
    analyze_market_value_by_area,
    analyze_prices
)


# create folder for saved charts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHART_DIR = os.path.join(BASE_DIR, "charts")

os.makedirs(CHART_DIR, exist_ok=True)



properties = get_properties()



# 1. Availability Chart

availability = analyze_availability(properties)

labels = [item[0] for item in availability]
values = [item[1] for item in availability]


plt.figure(figsize=(8,5))

plt.bar(labels, values)

plt.title("Property Availability Analysis")

plt.xlabel("Status")
plt.ylabel("Number of Properties")

plt.savefig(
    os.path.join(CHART_DIR, "availability_analysis.png")
)

plt.close()



# 2. Property Type Distribution

property_types = analyze_property_types(properties)

labels = [item[0] for item in property_types]
values = [item[1] for item in property_types]


plt.figure(figsize=(8,5))

plt.bar(labels, values)

plt.title("Property Type Distribution")

plt.xlabel("Property Type")
plt.ylabel("Number of Properties")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "property_type_distribution.png")
)

plt.close()



# 3. Top Locations

locations = analyze_location(properties)

# take top 10

locations = locations[:10]


labels = [item[0] for item in locations]
values = [item[1] for item in locations]


plt.figure(figsize=(10,6))

plt.barh(labels, values)

plt.title("Top Property Locations")

plt.xlabel("Number of Properties")

plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "top_locations.png")
)

plt.close()



# 4. Market Value By Area


market_values = analyze_market_value_by_area(properties)

market_values = market_values[:10]


labels = [item[0] for item in market_values]
values = [item[1] / 1_000_000 for item in market_values]


plt.figure(figsize=(10,6))

plt.barh(labels, values)

plt.title("Market Value By Area")

plt.xlabel("Total Value (Million ₦)")

plt.tight_layout()


plt.savefig(
    os.path.join(CHART_DIR, "market_value_by_area.png")
)

plt.close()



# 5. Price Analysis


average, highest, lowest = analyze_prices(properties)


labels = [
    "Average",
    "Highest",
    "Lowest"
]

values = [
    average / 1_000_000,
    highest / 1_000_000,
    lowest / 1_000_000
]


plt.figure(figsize=(7,5))


plt.bar(labels, values)


plt.title("Property Price Analysis")

plt.ylabel("Price (Million ₦)")


plt.savefig(
    os.path.join(CHART_DIR, "price_analysis.png")
)


plt.close()



print("All charts created successfully")