import re
from app.helpers import names


EXTRA = r'[\s&,+/()–-]'
THROWAWAY_VALUES = '|'.join((
    r'cells',
    rf"Condition{EXTRA}*Day",
    r'condition\s+of\s+NOT\s+0\.025',
    r'(?:d(?:ay)?)?(?:\s*in\s*culture)?',
    r'e6\/ml',
    r'each',
    r'IUPMs?',
    r'million\scells\/ml',
    r'N\/A',
    rf"{names.TABLE_NOTE}:",
    r'or',
    r'w',
))

THROWAWAY = re.compile(rf"""
    ^{EXTRA}*(?:{THROWAWAY_VALUES})*{EXTRA}*$|
    ^{EXTRA}*(D{EXTRA}*)+$
""", re.X | re.I)

UNICODES = {
    r'\uf067': '\N{GREEK SMALL LETTER GAMMA}',
    r'\uf064': '\N{GREEK SMALL LETTER DELTA}',
    r'\uf02d': '-',
    r'\uf02f': '/',
    r'\uf06d': '\N{GREEK SMALL LETTER MU}'
}


def get_unmatched_values(original, matched_values=None):
    unmatched = original
    if matched_values:
        matched_values.sort(key=len, reverse=True)

    for value in matched_values or []:
        unmatched = unmatched.replace(value, '', 1)

    unmatched = None if THROWAWAY.match(unmatched) else unmatched
    return unmatched


def replace_problematic_characters(value):
    for character, replacment in UNICODES.items():
        value = re.sub(character, replacment, value)

    value = re.sub(r'\s+', ' ', value)
    return value


def header_match(header, pattern):
    header = replace_problematic_characters(header)

    return pattern.match(header)


def match(value, pattern_list):
    if not value:
        return None

    if not isinstance(pattern_list, tuple):
        pattern_list = (pattern_list,)

    value = replace_problematic_characters(value)
    matched_dicts = []
    matched_values = []

    for pattern in pattern_list:
        matches = pattern.finditer(value)

        for m in matches:
            matched_dict = {k: v for (k, v) in m.groupdict().items() if v}
            matched_values.extend(matched_dict.values())

            matched_dicts.append(matched_dict)

    if matched_dicts:
        return {
            names.MATCHED: matched_dicts,
            names.UNMATCHED: get_unmatched_values(value, matched_values)
        }
    else:
        return {names.UNMATCHED: get_unmatched_values(value)}
