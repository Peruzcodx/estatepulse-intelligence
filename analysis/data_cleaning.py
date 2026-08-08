def clean_property_types(properties):
    cleaned_properties = []

    for property in properties:
        property_type = property[7]

        valid_types = [
            "Apartment",
            "Duplex",
            "Villa",
            "Office Space",
            "House",
            "Commercial Building",
            "Land"
        ]

        if property_type not in valid_types:
            property_type = "Land"

        cleaned_properties.append(property_type)

    return cleaned_properties
def clean_locations(location):

    if "Lekki" in location:
        return "Lekki"

    elif "Ikoyi" in location:
        return "Ikoyi"

    elif "Victoria Island" in location:
        return "Victoria Island"

    elif "Ikeja" in location:
        return "Ikeja"

    elif "Ajah" in location:
        return "Ajah"

    elif "Yaba" in location:
        return "Yaba"

    elif "GRA" in location:
        return "GRA"

    elif "FCT" in location:
        return "Abuja"

    elif "Asokoro" in location:
        return "Abuja"

    elif "Maitama" in location:
        return "Abuja"

    elif "Wuse" in location:
        return "Abuja"

    elif "Gwarinpa" in location:
        return "Abuja"

    elif "Kuje" in location:
        return "Abuja"

    elif "Katampe" in location:
        return "Abuja"

    else:
        return "Other"