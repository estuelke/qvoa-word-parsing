from app.helpers import names


# TODO: Refactor this method once all IUPM data has been matched
def clean_iupms(data):
    cols = [names.IUPM, names.DRUG_CONDITION, names.CONC, names.UNITS]
    check = all(item in data.columns for item in cols)
    cols = cols if check else [names.IUPM]

    clean = data.dropna(
        how='all',
        subset=cols
    )

    clean = clean.loc[data[names.IUPM] != 'N/A']
    return clean
