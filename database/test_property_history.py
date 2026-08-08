from database.history import get_property_history


property_id = "ecd543ff-fd35-49ab-9b8a-10bbbdb1041c"


history = get_property_history(property_id)


for item in history:
    print(item)