import os
from datetime import datetime

from analysis.market_analysis import (
    get_properties,
    analyze_prices,
    analyze_property_types,
    analyze_location,
    analyze_availability,
    analyze_price_by_type
)


def generate_report():

    properties = get_properties()

    average, highest, lowest = analyze_prices(properties)

    property_types = analyze_property_types(properties)

    locations = analyze_location(properties)

    availability = analyze_availability(properties)

    prices_by_type = analyze_price_by_type(properties)


    report = f"""
ESTATEPULSE MARKET INTELLIGENCE REPORT
======================================

Generated:
{datetime.now().strftime("%d %B %Y")}


Total Properties:
{len(properties)}


Average Property Price:
₦{average:,.0f}


Highest Property Price:
₦{highest:,.0f}


Lowest Property Price:
₦{lowest:,.0f}


Most Common Property Type:
{property_types[0][0]}


Top Locations:
"""
    for status, count in locations:
        report += f"{status}: {count} properties\n"  
        for location, count in locations:
            report += f"{location}: {count} properties\n"
    """


Availability Status:
"""


    for status, count in availability:
        report += f"{status}: {count}\n"


    report += "\n\nAverage Price By Property Type:\n"


    for property_type, price in prices_by_type:
        report += f"{property_type}: ₦{price:,.0f}\n"


    reports_folder = "reports"

    os.makedirs(
        reports_folder,
        exist_ok=True
    )


    report_path = os.path.join(
        reports_folder,
        "market_report.txt"
    )


    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report)


    print(
        f"Report generated successfully: {report_path}"
    )


if __name__ == "__main__":
    generate_report()