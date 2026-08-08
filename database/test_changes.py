from analysis.history_analysis import get_property_changes


changes = get_property_changes()


for item in changes[:10]:
    print(item)