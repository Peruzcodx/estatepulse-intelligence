from analysis.change_detector import detect_property_changes


property_id = "ecd543ff-fd35-49ab-9b8a-10bbbdb1041c"


changes = detect_property_changes(property_id)


print(changes)