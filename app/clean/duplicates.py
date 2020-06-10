from app.helpers import names


def get_max_indices(grp, criteria_col):
    return grp.loc[grp[criteria_col] == grp[criteria_col].max()]


def get_min_indices(grp, criteria_col):
    return grp.loc[grp[criteria_col] == grp[criteria_col].min()]


def annotate_duplicates_with_different_results(
    data,
    subset,
    criteria_col,
    qc_col,
    annotations=None,
    drop_duplicates=True,
    get_indices=(get_min_indices, get_max_indices)
):
    """
    Annotates rows that contain two sets of different data due to
    matching multiple values
    """
    default_cols = [names.PH, names.COL_ID, names.ROW_ID]
    cols = [*default_cols, *subset]

    dbl_data = data.loc[data[names.VALUE_MATCH] == 'FULL', cols]
    dbl_data = dbl_data.dropna(how='any', subset=subset)

    if drop_duplicates:
        dbl_data = dbl_data.drop_duplicates(subset=cols, keep=False)

    dbl_data = dbl_data.groupby(default_cols).filter(lambda grp: len(grp) > 1)
    dbl_data = dbl_data.groupby(default_cols, as_index=False)

    if not annotations:
        annotations = (
            'Value excludes contaminated wells or wells close to cutoff',
            'Value includes contaminated wells or wells close to cutoff'
        )

    for i in range(2):
        max_min_data = dbl_data.apply(
            lambda g: get_indices[i](g, criteria_col)
        )
        indices = max_min_data.index.get_level_values(1)
        data.loc[indices, qc_col] = annotations[i]

    return data


def annotate_duplicates_with_same_results(
    data, criteria_cols, annotation=None
):
    """
    Annotates rows with duplicated data (data same in both rows)
    """
    cols = [names.PH, names.COL_ID, names.ROW_ID, *criteria_cols]

    dupe_data = data.loc[data[names.VALUE_MATCH] == 'FULL', cols]
    dupe_data = dupe_data.dropna(how='any', subset=cols)
    dupe_data = dupe_data.duplicated(subset=cols, keep=False)
    indices = dupe_data[dupe_data].index

    data.loc[indices, names.WELL_QC] = \
        annotation if annotation else 'Data duplicated in original document'
    return data


def exclude_duplicated_results(data, criteria_cols):
    """
    Excludes any rows that are duplicates based on the criteria cols
    """
    cols = [names.PH, names.COL_ID, names.ROW_ID, *criteria_cols]

    dupe_data = data.loc[data[names.VALUE_MATCH] == 'FULL', cols]
    dupe_data = dupe_data.duplicated(subset=cols, keep='first')
    indices = dupe_data[dupe_data].index

    data.loc[indices, [names.WELL_QC, names.EXCLUDE_REASON]] = \
        'Duplicate data row likely due to multiple matching'
    data.loc[indices, names.EXCLUDE] = True
    print(dupe_data)
    return data
