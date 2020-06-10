from app.helpers import names
from app.clean.duplicates import annotate_duplicate_results


def exclude(data):
    data = data.copy()
    m1 = data[names.RAW_VALUE] == 'X'
    data.loc[m1, names.UNMATCHED] = None
    data.loc[m1, names.VALUE_MATCH] = 'FULL'
    data.loc[m1, names.EXCLUDE] = True
    data.loc[m1, names.EXCLUDE_REASON] = 'Indicates there is no value'

    return data


def clean(raw_data):
    data = raw_data.copy()
    data = data.astype({names.IUPM: float}, errors='ignore')
    data = annotate_duplicate_results(
        data, [names.IUPM], names.IUPM, names.IUPM_QC)
    data = exclude(data)
    return data
