import sqlite3
import os

from analysis.data_cleaning import clean_property_types
from analysis.current_market import get_current_properties

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(
    BASE_DIR,
    "..",
    "database",
    "estatepulse.db"
)


def get_properties():

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
    SELECT *
    FROM property_snapshots
    WHERE id IN (
        SELECT MAX(id)
        FROM property_snapshots
        GROUP BY property_id
    )
    """)

    properties = cursor.fetchall()

    connection.close()

    return properties


def clean_price(price):

    price = price.replace("₦", "")
    price = price.replace(",", "")

    return int(price)


def analyze_prices(properties):

    if len(properties) == 0:
        return 0, 0, 0

    cleaned_price = []

    for property in properties:

        price = clean_price(property[2])

        cleaned_price.append(price)


    average_price = sum(cleaned_price) / len(cleaned_price)

    highest = max(cleaned_price)

    lowest = min(cleaned_price)


    return average_price, highest, lowest

def analyze_location(properties):

    location_count = {}

    for property in properties:

        area = property[3]

        if area in location_count:

            location_count[area] += 1

        else:

            location_count[area] = 1

    sorted_locations = sorted(
        location_count.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return sorted_locations
   


def analyze_property_types(properties):

    cleaned_types = clean_property_types(properties)

    property_type_count = {}


    for property_type in cleaned_types:

        if property_type in property_type_count:

            property_type_count[property_type] += 1

        else:

            property_type_count[property_type] = 1



    sorted_property_types = sorted(
        property_type_count.items(),
        key=lambda item: item[1],
        reverse=True
    )


    return sorted_property_types



def analyze_availability(properties):

    availability_count = {}


    for property in properties:

        availability = property[8]


        if availability in availability_count:

            availability_count[availability] += 1

        else:

            availability_count[availability] = 1



    sorted_availability = sorted(
        availability_count.items(),
             key=lambda item: item[1],
        reverse=True
    )


    return sorted_availability



def analyze_price_by_type(properties):

    cleaned_types = clean_property_types(properties)

    property_prices = {}


    for property, property_type in zip(properties, cleaned_types):

        price = clean_price(property[2])


        if property_type in property_prices:

            property_prices[property_type].append(price)

        else:

            property_prices[property_type] = [price]



    average_prices = {}


    for property_type, prices in property_prices.items():

        average_prices[property_type] = sum(prices) / len(prices)



    sorted_prices = sorted(
        average_prices.items(),
        key=lambda item: item[1],
        reverse=True
    )


    return sorted_prices


def analyze_market_value_by_area(properties):

    area_values = {}

    for property in properties:

        area = property[3]

        price = clean_price(property[2])

        if area in area_values:

            area_values[area] += price

        else:

            area_values[area] = price


    sorted_values = sorted(
        area_values.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return sorted_values
 

if __name__ == "__main__":

    properties = get_current_properties()


    print(f"Total properties: {len(properties)}")


    average, highest, lowest = analyze_prices(properties)


    print(f"Average price: ₦{average:,.0f}")

    print(f"Highest price: ₦{highest:,.0f}")

    print(f"Lowest price: ₦{lowest:,.0f}")



    locations = analyze_location(properties)


    print("\nTop Locations\n")


    for location, count in locations:

        print(f"{location}: {count} properties")



    property_types = analyze_property_types(properties)


    print("\nProperty Types\n")

    print(f"Property types count: {len(property_types)}")


    for property_type, count in property_types:

        print(f"{property_type}: {count}")



    print("\nAvailability\n")


    availability = analyze_availability(properties)


    for availability_status, count in availability:

          print(f"{availability_status}: {count}")


    market_values = analyze_market_value_by_area(properties)

    print("\nMarket Value By Area\n")

    for area, value in market_values:

      print(f"{area}: ₦{value:,.0f}")


def analyze_price_segments(properties):

    segments = {
        "Budget": 0,
        "Mid Range": 0,
        "Luxury": 0
    }

    for property in properties:

        price = int(
            property[2]
            .replace("₦", "")
            .replace(",", "")
        )

        if price < 50_000_000:

            segments["Budget"] += 1

        elif price < 200_000_000:

            segments["Mid Range"] += 1

        else:

            segments["Luxury"] += 1

    return list(segments.items())
def extract_area(location):
    location = location.lower()

    areas = [
        "lekki",
        "victoria island",
        "ikoyi",
        "ajah",
        "ikeja",
        "yaba",
        "asokoro",
        "maitama",
        "wuse",
        "gwarinpa",
        "ibadan",
        "port harcourt",
        "amuwo",
        "ogudu"
    ]

    for area in areas:
        if area in location:
            return area.title()

    return "Other"


def analyze_areas(properties):

    areas = {}

    for property in properties:

        location = property[3]

        area = extract_area(location)

        areas[area] = areas.get(area, 0) + 1

    return sorted(
        areas.items(),
        key=lambda x:x[1],
        reverse=True
    )