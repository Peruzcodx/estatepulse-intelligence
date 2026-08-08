from analysis.history_analysis import get_latest_properties


properties = get_latest_properties()


print("Total current properties:", len(properties))


for key, value in list(properties.items())[:5]:
    print(key, value)