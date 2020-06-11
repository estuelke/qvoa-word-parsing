import re
from app.helpers import names
from app.clean.all_data import exclude_partial_full_match_duplicates


UNMATCHED_DRUG_VALUES = re.compile(
    rf"^[\(\)\s]+(?:PHA|335|250)[\s\)]+$",
    re.I
)


def fix_unmatched_values(data):
    unmatched = data.copy()
    unmatched = unmatched.loc[unmatched[names.UNMATCHED].notna()]

    m1 = (unmatched[names.UNMATCHED].str.contains(UNMATCHED_DRUG_VALUES))
    indices = unmatched[m1].index

    data.loc[indices, names.VALUE_MATCH] = 'FULL'
    data.loc[indices, names.UNMATCHED] = None
    data.loc[indices, names.DRUG_QC] = \
        'Removed unmatched value because value was redundant'

    return data


def clean(raw_data):
    data = raw_data.copy()
    data = fix_unmatched_values(data)
    data = exclude_partial_full_match_duplicates(data)

    return data
