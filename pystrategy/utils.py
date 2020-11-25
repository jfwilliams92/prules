import datetime
ACCEPTED_DATE_PATTERNS = ["%d-%m-%Y", "%Y-%m-%d", "%m/%d/%Y", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d %H:%M:%S.%f"]

def detect_date(date_string):
    """Detect datetime string and parse to python datetime.

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