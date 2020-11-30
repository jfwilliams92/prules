import datetime
import numpy as np
import json

ACCEPTED_DATE_PATTERNS = [
    "%d-%m-%Y", 
    "%Y-%m-%d", 
    "%m/%d/%Y", 
    "%Y-%m-%dT%H:%M:%S.%fZ", 
    "%Y-%m-%d %H:%M:%S.%f"
]

def parse_date(date_string):
    """Detect datetime string from accepted pattern and parse to python datetime.

    Args:
        date_string (str): datetime string
    
    Returns:
        match (bool): whether or not the string could be parsed by accepted patterns
        datetime (datetime.datetime): parsed python datetime.
    """

    for pattern in ACCEPTED_DATE_PATTERNS:
        try:
            return True, datetime.datetime.strptime(date_string, pattern)
        except:
            pass 

    return False, None

def detect_date_field(field_value):
    """Detect whether incoming field value is datetime and parse as appropriate.
    If incoming value is a list, attempt to parse every item in the list.
    If every list item can be parsed, then return parsed values.
    If some of the items are dates and others are not, fails datetime detection.

    Args:
        field_value (str/float/list): incoming field value
    """
    if isinstance(field_value, list):
        is_date = []
        parsed_fields = []
        for item in field_value:
            rez = parse_date(item)
            is_date.append(rez[0])
            parsed_fields.append(rez[1] or item)

        if np.array(is_date).all():
            return True, parsed_fields

    return parse_date(field_value)

def pluck(payload, path):
    """Pluck a field out via path delimited by '.'"""
    path_parts = path.split('.')
    for part in path_parts:
        if not isinstance(payload, dict):
            return None
        payload = payload.get(part, None)

    return payload

def dict_from_json(json_str):
    return json.loads(json_str)

def dict_from_json_file(path):
    with open(path) as f:
        return json.load(f)