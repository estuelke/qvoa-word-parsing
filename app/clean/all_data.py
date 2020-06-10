import pandas as pd
from app.helpers import names


def exclude_partial_full_match_duplicates(data):
    keep_cols = [names.PH, names.CELL, names.HEADER_MATCH, names.VALUE_MATCH]
    all_matches = data.loc[:, keep_cols]

    non_matches = all_matches.loc[all_matches[
        names.VALUE_MATCH].isin(['PARTIAL', None])
    ].reset_index()
    full_matches = all_matches.loc[all_matches[names.VALUE_MATCH] == 'FULL']

    subset = [names.PH, names.CELL, names.HEADER_MATCH]
    full_matches = full_matches.drop_duplicates(subset=subset)
    common_rows = pd.merge(
        non_matches, full_matches, on=subset, how='inner'
    )

    indices_to_exclude = list(common_rows['index'])
    data.loc[indices_to_exclude, names.EXCLUDE] = True
    data.loc[indices_to_exclude, names.EXCLUDE_REASON] = \
        'This is a non/partial match where a full match exists'

    return data


def fix_incorrectly_identified_dilution_header(data):
    data = data.copy()
    m1 = (data[names.PH] == '120')
    m2 = (data[names.ROW_ID] == '15')
    m3 = (data[names.COL_ID] == 'A')
    index = data.loc[m1 & m2 & m3].index

    data.loc[index, names.DILN] = '0.0125'
    data.loc[index, names.DILUTION_QC] = \
        'Header incorrectly labeled as IUPM instead of 0.0125'
    return data


def clean(raw_data):
    data = raw_data.copy()
    data = exclude_partial_full_match_duplicates(data)
    data.loc[data[names.RAW_VALUE].isna(), names.EXCLUDE] = True
    data.loc[data[names.RAW_VALUE].isna(), names.EXCLUDE_REASON] = \
        'No value to process'

    data = fix_incorrectly_identified_dilution_header(data)
    return data
