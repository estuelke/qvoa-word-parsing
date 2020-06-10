import re
from app.helpers import names

FIX_DOT_DELIMITER = re.compile(r'(?P<Positive>\d)\.(?P<Total>\d)')
FIX_MISSING_DELIMITER = re.compile(r'(?P<Positive>[04]|12)(?P<Total>6|18)')


def fix_typos(data):
    # Typo: Experiment PH342 Cell C10
    m = (data[names.POSITIVE] == 'i')
    data.loc[m, names.WELL_QC] = 'Raw Value (i/6) has typo: i changed to 1'
    data.loc[m, names.POSITIVE] = 1

    # Typo: Experiment PH365 Cell E10
    m1 = (data[names.RAW_VALUE] == '35639')
    m2 = (data[names.CELL] == 'E10')
    m3 = (data[names.PH] == '365')
    index = data.loc[m1 & m2 & m3].index

    data.loc[index, names.POSITIVE] = '36'
    data.loc[index, names.TOTAL] = '39'
    data.loc[index, names.VALUE_MATCH] = 'FULL'
    data.loc[index, names.UNMATCHED] = None
    data.loc[index, names.WELL_QC] = """
        Raw value (35639) incorrect: should be 36 (Positive) & 39 (Total).
        Based on previous value and increased IUPM value.
    """

    # Typo: Experiment PH362 Cell B4
    m1 = (data[names.RAW_VALUE] == '216')
    m2 = (data[names.CELL] == 'B4')
    m3 = (data[names.PH] == '362')
    index = data.loc[m1 & m2 & m3].index

    data.loc[index, names.POSITIVE] = '2'
    data.loc[index, names.TOTAL] = '6'
    data.loc[index, names.VALUE_MATCH] = 'FULL'
    data.loc[index, names.UNMATCHED] = None
    data.loc[index, names.WELL_QC] = \
        'Original value should be 2/6. 1 incorrectly input instead of /.'

    return data


def fix_dot_delimiter(data):
    phs = ['209', '229', '252', '256']
    index = data.loc[
        data[names.PH].isin(phs) & data[names.UNMATCHED].notna()].index

    data.loc[index, [names.POSITIVE, names.TOTAL]] = \
        data.loc[index][names.UNMATCHED].str.extract(FIX_DOT_DELIMITER)

    data.loc[index, names.UNMATCHED] = None
    data.loc[index, names.VALUE_MATCH] = 'FULL'
    data.loc[index, names.WELL_QC] = \
        'Delimiter incorrectly typed as . instead of /'

    return data


def fix_missing_delimiter(data):
    phs = ['32', '63', '258', '346']
    index = data.loc[
        data[names.PH].isin(phs) & data[names.UNMATCHED].notna()].index

    data.loc[index, [names.POSITIVE, names.TOTAL]] = \
        data.loc[index][names.UNMATCHED].str.extract(FIX_MISSING_DELIMITER)

    data.loc[index, names.UNMATCHED] = None
    data.loc[index, names.VALUE_MATCH] = 'FULL'
    data.loc[index, names.WELL_QC] = \
        'Delimiter (/) missing in original value'
    return data


def exclude_non_well_values(data):
    m1 = (data[names.RAW_VALUE] == '0.819')
    m2 = (data[names.CELL] == 'C13')
    m3 = (data[names.PH] == '142')
    index = data.loc[m1 & m2 & m3].index

    data.loc[index, names.UNMATCHED] = None
    data.loc[index, names.EXCLUDE] = True
    data.loc[index, names.EXCLUDE_REASON] = \
        'See Well QC Note'
    data.loc[index, names.WELL_QC] = \
        'Value incorrectly input in a well cell. Repeat of IUPM below.'

    return data


def get_multi_row_groups(grp):
    return len(grp) > 1


def get_multi_row_groups_with_equivalent_totals(grp):
    return len(grp) > 1 and grp[names.TOTAL].max() == grp[names.TOTAL].min()


def annotate_wells_with_double_results(
    data, subset, criteria_col, filter_func, max_annotation, min_annotation
):
    default_cols = [names.PH, names.COL_ID, names.ROW_ID]
    cols = [*default_cols, *subset]

    dbl_data = data.loc[data[names.VALUE_MATCH] == 'FULL', cols]
    dbl_data = dbl_data.dropna(how='any', subset=subset)
    dbl_data = dbl_data.drop_duplicates(subset=cols, keep=False)
    dbl_data = dbl_data.groupby(default_cols).filter(filter_func)

    dbl_data = dbl_data.groupby(default_cols, as_index=False)
    dbl_data_max = dbl_data.apply(
        lambda g: g.loc[g[criteria_col] == g[criteria_col].max()]
    )
    dbl_data_min = dbl_data.apply(
        lambda g: g.loc[g[criteria_col] == g[criteria_col].min()]
    )

    max_indices = dbl_data_max.index.get_level_values(1)
    min_indices = dbl_data_min.index.get_level_values(1)
    data.loc[max_indices, names.WELL_QC] = max_annotation
    data.loc[min_indices, names.WELL_QC] = min_annotation

    return data


def annotate_wells_with_duplicate_results(data):
    cols = [names.PH, names.COL_ID, names.ROW_ID, names.POSITIVE, names.TOTAL]

    dupe_data = data.loc[data[names.VALUE_MATCH] == 'FULL', cols]
    dupe_data = dupe_data.dropna(how='any', subset=cols)
    dupe_data = dupe_data.duplicated(subset=cols, keep=False)
    indices = dupe_data[dupe_data].index

    data.loc[indices, names.WELL_QC] = \
        'Data was duplicated in original document'
    return data


def fix_partial_match_due_to_comment_symbol(data):
    m1 = (data['Pheresis'] == '10')
    m2 = (data['Column ID'] == 'G')
    m3 = (data['Row ID'] == '11')

    well = data.loc[m1 & m2 & m3]

    indices_to_exclude = well.loc[well[names.WELL_SYMBOL].isna()].index
    data.loc[indices_to_exclude, names.EXCLUDE] = True
    data.loc[indices_to_exclude, names.EXCLUDE_REASON] = \
        'This is a non/partial match where a full match exists'

    index_to_fix = well.loc[well[names.WELL_SYMBOL].notna()].index
    data.loc[index_to_fix, names.UNMATCHED] = None
    data.loc[index_to_fix, names.VALUE_MATCH] = 'FULL'

    return data


def clean(raw_data):
    data = raw_data.copy()
    data = data.astype(
        {names.POSITIVE: 'int64', names.TOTAL: 'int64'}, errors='ignore'
    )
    data = fix_typos(data)
    data = fix_dot_delimiter(data)
    data = fix_missing_delimiter(data)
    data = exclude_non_well_values(data)
    data = annotate_wells_with_double_results(
        data, [names.TOTAL], names.TOTAL, get_multi_row_groups,
        'Positive/Total contain contaminated wells',
        'Positive/Total contain only non-contaminated wells'
    )
    data = annotate_wells_with_double_results(
        data, [names.POSITIVE, names.TOTAL], names.POSITIVE,
        get_multi_row_groups_with_equivalent_totals,
        'Positive contain wells near cutoff (needs verification)',
        'Positive does not contain wells near cutoff (needs verification)'
    )
    data = annotate_wells_with_duplicate_results(data)
    data = fix_partial_match_due_to_comment_symbol(data)
    return data
