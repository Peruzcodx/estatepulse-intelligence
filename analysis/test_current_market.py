from analysis.current_market import get_current_properties


properties = get_current_properties()


print(f"Current properties: {len(properties)}")


for property in properties[:5]:
    print(property)