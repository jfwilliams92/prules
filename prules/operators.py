import re

def between(a, b):
    """Evaluates a between b[0] and b[1]"""
    # since reading from JSON, values are either string, float, or list of values
    if not isinstance(b, list):
        raise TypeError('other value must be a list of length 2')
    
    return b[0] <= a <= b[1]

def not_between(a, b):
    """Evaluates a not between b[0] and b[1]"""
    if not isinstance(b, list):
        raise TypeError('other value must be a list of length 2')

    result = b[0] <= a <= b[1]
    return False if result else True

def in_(a, b):
    return a in b

def not_in(a, b):
    """Evalutes a not in b"""
    result = False if a in b else True
    return result

def not_contains(a, b):
    """Evaluates a does not contain b"""
    result = False if b in a else True
    return result

def re_contains(a, b):
    """Return True if a regex search with pattern b yields a match in a

    Args:
        a (str): Pattern to search
        b (str): Regex pattern to use in search

    Returns:
        result (bool): Whether b contains a or not.
    """

    try:
        regexp = re.compile(b, flags=re.IGNORECASE)
    except(TypeError):
        raise TypeError('Value must be a string that can be compiled to regex expression')

    return bool(re.search(regexp, a))
