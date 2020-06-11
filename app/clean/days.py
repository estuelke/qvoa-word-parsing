import re
from app.helpers import names

DOUBLE_DAY = re.compile(r'17\/21')
EXCLUDE = re.compile(r'\s*\(0\)\s*')


def exclude_non_day_matches(data):
    data = data.copy()
    m1 = (data[names.UNMATCHED].notna())
    m2 = (data[names.UNMATCHED].str.match(EXCLUDE))

    indices = data.loc[m1 & m2].index
    data.loc[indices, names.EXCLUDE] = True
    data.loc[indices, names.EXCLUDE_REASON] = \
        'Original value does not contain a day value'

    return data


def annotate_double_day_result(data):
    data = data.copy()
    m1 = (data[names.DAY].notna())
    m2 = (data[names.DAY].str.match(DOUBLE_DAY))

    indices = data.loc[m1 & m2].index
    data.loc[indices, names.DAY_QC] = \
        'Manually verify the correct day is associated with this data'

    return data


def clean(raw_data):
    data = raw_data.copy()
    data = exclude_non_day_matches(data)

    return data
