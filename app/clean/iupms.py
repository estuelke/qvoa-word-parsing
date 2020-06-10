from app.helpers import names
from app.clean.duplicates import annotate_duplicate_results


def clean(raw_data):
    data = raw_data.copy()
    data = data.astype({names.IUPM: float}, errors='ignore')
    data = annotate_duplicate_results(
        data, [names.IUPM], names.IUPM, names.IUPM_QC)
    return data
