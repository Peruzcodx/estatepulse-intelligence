from database.history import save_snapshot


def save_property(property_data):
    """
    Save one property snapshot to the database.

    The actual database insertion is handled by save_snapshot()
    so that every property is recorded only once.
    """

    save_snapshot(property_data)