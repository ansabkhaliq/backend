"""
Json(Dict) validator
"""


def lack_keys(data, required_keys):
    if data is None:
        return ', '.join(required_keys)
    keys = ', '.join(filter(lambda key: key not in data, required_keys))
    return keys


# Todo check type
def check_keys_type(data, key_type_map):
    pass
