import pandas as pd
from app.helpers import names
from app.clean import wells


def clean_info(info):
    info = info.copy()
    info[names.EXTRA] = info.loc[:, names.EXTRA].apply(
        lambda x: None if x == [None] else x
    )

    return info


# def clean_iupms(data):
#     cols = [names.IUPM, names.DRUG_CONDITION, names.CONC, names.UNITS]
#     check = all(item in data.columns for item in cols)
#     cols = cols if check else [names.IUPM]

#     clean = data.dropna(
#         how='all',
#         subset=cols
#     )

#     clean = clean.loc[data[names.IUPM] != 'N/A']
#     return {
#         names.CLEAN: clean,
#         names.QUARANTINED: get_quarantined(data, clean)
#     }


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


DEFAULT_COLUMNS = [
    names.PH,
    names.FILE,
    names.CELL,
    names.COL_ID,
    names.ROW_ID,
    names.HEADER_MATCH,
    names.HEADER,
    names.VALUE_MATCH,
    names.UNMATCHED,
    names.RAW_VALUE,
    names.EXCLUDE,
    names.EXCLUDE_REASON
]

RESULTS_MAP = (
    {'name': names.UNMATCHED},
    {'name': names.DAY_DATA, 'header': names.DAY, 'columns': [names.DAY]},
    {'name': names.DRUG_DATA, 'columns': [
            names.DRUG_CONDITION, names.CONC, names.UNITS, names.DRUG_NOTE
        ]},
    {'name': names.INFO, 'header': names.INFO,
        # 'clean': clean_info
        },
    {'name': names.IUPM_DATA, 'header': names.IUPM,
        'columns': [names.IUPM_MODIFIER, names.IUPM, names.IUPM_NOTE]},
    {'name': names.WELL_DATA, 'header': names.DILN, 'columns': [
            names.POSITIVE, names.TOTAL, names.P24_RESULT, names.WELL_NOTE,
            names.WELL_SYMBOL
        ],
        'clean': wells.clean},
)


def filter_results(data, columns, header):
    col_mask = (data[columns].notna().any(1)) if columns else None
    header_mask = (data[names.HEADER_MATCH] == header) if header else None

    if columns and header:
        data = data.loc[col_mask | header_mask]
    elif header:
        data = data.loc[header_mask]
    elif columns:
        data = data.loc[col_mask]

    columns = [*DEFAULT_COLUMNS, *columns]
    data = data.loc[:, columns]
    return data


def distribute_and_clean_data(raw_data):
    data = raw_data.copy()
    data = exclude_partial_full_match_duplicates(data)
    data.loc[data[names.RAW_VALUE].isna(), names.EXCLUDE] = True
    data.loc[data[names.RAW_VALUE].isna(), names.EXCLUDE_REASON] = \
        'No value to process'
    final = {
        names.ALL_DATA: {
            names.RAW: raw_data,
            names.CLEAN: data
        },
    }

    for result in RESULTS_MAP:
        columns = result.get('columns', [])
        header = result.get('header', None)
        result_raw_data = filter_results(data, columns, header)

        clean_func = result.get('clean', None)
        clean_data = result_raw_data.loc[result_raw_data[names.EXCLUDE].isna()]

        if clean_func:
            clean_data = clean_func(clean_data)
            excluded_indexes = clean_data.loc[
                clean_data[names.EXCLUDE].notna()
            ].index
            result_raw_data.loc[
                excluded_indexes, [names.EXCLUDE, names.EXCLUDE_REASON]] = \
                clean_data[[names.EXCLUDE, names.EXCLUDE_REASON]]
            clean_data = clean_data.loc[clean_data[names.EXCLUDE].isna()]

        name = result['name']
        final[name] = {
            names.RAW: result_raw_data,
            names.CLEAN: clean_data
        }

    return final
