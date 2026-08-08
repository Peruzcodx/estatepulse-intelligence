from datetime import datetime
from playwright.sync_api import sync_playwright

from database.save_data import save_property


# =====================================================
# STORAGE
# =====================================================

all_property = []
property_data = []


# =====================================================
# START PLAYWRIGHT
# =====================================================

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()


    # =================================================
    # GET PROPERTY LINKS
    # =================================================

    page.goto(
        "https://estate-pulse-nigeria.lovable.app/properties"
    )

    page.wait_for_load_state("networkidle")


    links = page.locator(
        "a[href^='/properties/']"
    ).all()


    for link in links:

        href = link.get_attribute("href")

        if href:

            complete_url = (
                f"https://estate-pulse-nigeria.lovable.app{href}"
            )

            if complete_url not in all_property:

                all_property.append(
                    complete_url
                )


    print(
        f"Successfully found {len(all_property)} properties"
    )


    # =================================================
    # SCRAPE EACH PROPERTY
    # =================================================

    for url in all_property:

        try:

            page.goto(url)

            page.wait_for_load_state("networkidle")


            # =============================================
            # BASIC INFORMATION
            # =============================================

            title = (
                page.locator("h1")
                .first
                .inner_text()
                .strip()
            )


            price = (
                page.locator("p.font-display")
                .first
                .inner_text()
                .strip()
            )


            location = (
                page.locator("p.mt-2")
                .first
                .inner_text()
                .strip()
            )


            # =============================================
            # PROPERTY DETAILS
            # =============================================

            details = page.locator("p.mt-3")

            detail_count = details.count()

            detail_values = []


            for i in range(detail_count):

                value = (
                    details
                    .nth(i)
                    .inner_text()
                    .strip()
                )

                detail_values.append(value)


            print("\n--------------------------------")
            print(f"Scraping: {title}")
            print(f"URL: {url}")
            print(
                f"Details found: {detail_values}"
            )


            # =============================================
            # DETECT LAND
                        # =============================================
            is_land = any(
                value.lower() == "land"
                for value in detail_values
            )


            # =============================================
            # LAND PROPERTY
            # =============================================

            if is_land:

                bedroom = "N/A"

                bathroom = "N/A"

                size = "N/A"

                availability = "N/A"

                apartment_type = "Land"


                for value in detail_values:

                    value_lower = value.lower()


                    # -----------------------------
                    # LAND SIZE
                    # -----------------------------

                    if "sqm" in value_lower:

                        size = value


                    # -----------------------------
                    # AVAILABILITY
                    # -----------------------------

                    elif value_lower in [
                        "available",
                        "sold",
                        "unavailable"
                    ]:

                        availability = value


            # =============================================
            # NORMAL / COMMERCIAL PROPERTY
            # =============================================

            else:

                bedroom = (
                    detail_values[0]
                    if len(detail_values) > 0
                    else "N/A"
                )


                bathroom = (
                    detail_values[1]
                    if len(detail_values) > 1
                    else "N/A"
                )


                size = (
                    detail_values[2]
                    if len(detail_values) > 2
                    else "N/A"
                )


                apartment_type = (
                    detail_values[3]
                    if len(detail_values) > 3
                    else "N/A"
                )


                availability = (
                    detail_values[4]
                    if len(detail_values) > 4
                    else "N/A"
                )


            # =============================================
            # PROPERTY ID
            # =============================================

            property_id = (
                url.rstrip("/")
                .split("/")[-1]
            )


            # =============================================
            # STORE DATA
            # =============================================

            stored_data = {

                "property_id": property_id,

                "title": title,

                "price": price,

                "location": location,

                "bedroom": bedroom,

                "bathroom": bathroom,

                "size": size,

                "apartment_type": apartment_type,

                "availability": availability,

                "url": url,

                "date_scraped":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
            }


            # =============================================
            # DISPLAY RESULT
            # =============================================

            print("\nSuccessfully scraped:")

            print(
                f"Title: {title}"
            )

            print(
                f"Bedroom: {bedroom}"
            )

            print(
                f"Bathroom: {bathroom}"
            )

            print(
                f"Size: {size}"
            )

            print(
                f"Type: {apartment_type}"
            )

            print(
                f"Availability: {availability}"
            )

            print(
                f"Property ID: {property_id}"
            )


            # =============================================
            # SAVE TO DATABASE
            # =============================================

            save_property(
                stored_data
            )

            property_data.append(
                stored_data
            )


        except Exception as e:

            print(
                f"\nERROR scraping {url}"
            )

            print(e)


    # =================================================
    # CLOSE BROWSER
    # =================================================

    browser.close()


# =====================================================
# FINAL RESULT
# =====================================================

print(
    f"\n{len(property_data)} properties successfully scraped"
)