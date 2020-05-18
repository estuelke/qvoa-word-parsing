from app.helpers import names


def check_drug_conditions(info, data, note):
    checks = []
    data_groups = data.groupby(names.PH)

    for name, row in info.iterrows():
        data = data_groups.get_group(name)
        drug_groups = data.groupby(names.ORIGINAL_DRUG)
        data_conditions = list(drug_groups.groups.keys())
        info_conditions = info.loc[name, names.DRUG_CONDITIONS]

        if data_conditions != info_conditions:
            checks.append({
                names.PH: name,
                names.EXPECTED: info_conditions,
                names.ACTUAL: data_conditions,
                names.NOTE: note,
            })

    return checks


def check_iupms(iupms):
    checks = []
    none_iupms = iupms.loc[iupms[names.IUPM].isna()]

    for _, row in none_iupms.iterrows():
        checks.append({
            names.PH: row[names.PH],
            names.EXPECTED: f"Non-null IUPM for {row[names.DRUG_CONDITION]} on Day {row[names.DAY]}",
            names.ACTUAL: row[names.IUPM],
            names.NOTE: 'Check Word Document for non-null IUPM',
        })

    return checks


def check_for_no_data(data, data_type):
    checks = []
    grouped = data.groupby([names.PH, names.RAW_DRUG])

    for (pheresis, drug), df in grouped:
        if df[names.RAW_VALUE].isna().all():
            checks.append({
                names.PH: pheresis,
                names.PH: f"No {data_type} values found for all days of {drug}"
            })
    return checks


def perform_qc(data):
    info = data[f"Clean {names.PH_INFO}"]
    iupms = data[f"Clean {names.IUPM_DATA}"]
    wells = data[f"Clean {names.WELL_DATA}"]
    qc_checks = []

    qc_checks.extend(check_drug_conditions(info, iupms, 'IUPM Data'))
    qc_checks.extend(check_iupms(iupms))
    qc_checks.extend(check_for_no_data(wells, 'Well'))
    qc_checks.extend(check_for_no_data(iupms, 'IUPM'))
    return qc_checks


# Notes:
# Empty Drug Condition
