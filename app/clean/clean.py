from app.helpers import names
from app.clean import all_data, days, drugs, iupms, wells


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


def unmatched_clean(data):
    data = data.copy()
    m1 = (data[names.UNMATCHED].notna())
    data = data.loc[m1]
    return data


RESULTS_MAP = (
    {
        'name': names.UNMATCHED,
        'clean': unmatched_clean
    },
    {
        'name': names.DAY_DATA,
        'header': names.DAY,
        'columns': [names.DAY, names.DAY_NOTE],
        'clean': days.clean
    },
    {
        'name': names.DILUTION_DATA,
        'columns': [names.DILN, names.DILUTION_QC]
    },
    {
        'name': names.DRUG_DATA,
        'columns': [
            names.DRUG_CONDITION, names.CONC, names.UNITS, names.DRUG_NOTE
        ],
        'clean': drugs.clean
    },
    {
        'name': names.INFO,
        'header': names.INFO
    },
    {
        'name': names.IUPM_DATA,
        'header': names.IUPM,
        'columns': [names.IUPM_MODIFIER, names.IUPM, names.IUPM_NOTE],
        'clean': iupms.clean
    },
    {
        'name': names.TABLE_NOTE,
        'header': names.TABLE_NOTE,
        'columns': [names.TABLE_NOTE]
    },
    {
        'name': names.WELL_DATA,
        'header': names.DILN,
        'columns': [
            names.POSITIVE, names.TOTAL, names.P24_RESULT, names.WELL_NOTE,
            names.WELL_SYMBOL
        ],
        'clean': wells.clean
    },
)


def filter_results(data, columns, header):
    col_mask = (data[columns].notna().any(1)) if columns else False
    header_mask = (data[names.HEADER_MATCH] == header) if header else False

    if columns or header:
        data = data.loc[col_mask | header_mask]

    columns = [*DEFAULT_COLUMNS, *columns]
    data = data.loc[:, columns]
    return data


def remove_excluded_rows(clean, raw):
    excluded_indexes = clean.loc[clean[names.EXCLUDE].notna()].index
    raw.loc[excluded_indexes, [names.EXCLUDE, names.EXCLUDE_REASON]] = \
        clean[[names.EXCLUDE, names.EXCLUDE_REASON]]
    clean = clean.loc[clean[names.EXCLUDE].isna()]

    return clean, raw


def distribute_and_clean_data(raw_data):
    data = all_data.clean(raw_data)

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
            clean_data, result_raw_data = remove_excluded_rows(
                clean_data, result_raw_data
            )

        name = result['name']
        final[name] = {
            names.RAW: result_raw_data,
            names.CLEAN: clean_data
        }

    return final
