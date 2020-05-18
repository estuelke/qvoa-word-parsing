import pytest  # Noqa: F401
from app.helpers import names
from app.patterns import drugs, iupms
from app.match import match
from app.cell import process_cell

drug_conditions = [
    ('PHA',
        drugs.ANY_ORDER,
        [{names.DRUG_CONDITION: 'PHA'}], None
     ),
    ('PHA 1ug/ml',
        drugs.ANY_ORDER, [{
            names.DRUG_CONDITION: 'PHA',
            names.CONC: '1',
            names.UNITS: 'ug/ml',
        }], None),
    ('PHA (1ug/ml)',
        drugs.ANY_ORDER, [{
            names.DRUG_CONDITION: 'PHA',
            names.CONC: '1',
            names.UNITS: 'ug/ml',
        }],
        None),
    ('PHA 1.5ug/ml',
        drugs.ANY_ORDER, [{
            names.DRUG_CONDITION: 'PHA',
            names.CONC: '1.5',
            names.UNITS: 'ug/ml',
        }], None),
    ('DMSO (0.005)',
        drugs.ANY_ORDER, [{
            names.DRUG_CONDITION: 'DMSO',
            names.CONC: '0.005',
        }], None),
    ('DMSO (%)',
        drugs.ANY_ORDER, [{
            names.DRUG_CONDITION: 'DMSO',
            names.UNITS: '%',
        }], None),
    ('SAHA 250',
        drugs.ANY_ORDER, [{
            names.DRUG_CONDITION: 'SAHA',
            names.CONC: '250',
        }], None),
    ('DMSO (0.005%)',
        drugs.ANY_ORDER, [{
            names.DRUG_CONDITION: 'DMSO',
            names.CONC: '0.005',
            names.UNITS: '%',
        }], None),
    ('AZD (nM)',
        drugs.ANY_ORDER, [{
            names.DRUG_CONDITION: 'AZD',
            names.UNITS: 'nM',
        }], None),
    ('AZD (20nM)',
        drugs.ANY_ORDER, [{
            names.DRUG_CONDITION: 'AZD',
            names.CONC: '20',
            names.UNITS: 'nM',
        }], None),
    ('AZD + Rx',
        drugs.ANY_ORDER, [{
            names.DRUG_CONDITION: 'AZD',
            names.ANTIRETROVIRALS: 'Rx',
        }], None),
    ('Tamox Total Resting',
        drugs.ANY_ORDER, [{
            names.DRUG_CONDITION: 'Tamox',
            names.CELL_CONDITION: 'Total Resting',
        }], None),
    ('Tamox Total Rest',
        drugs.ANY_ORDER, [{
            names.DRUG_CONDITION: 'Tamox',
            names.CELL_CONDITION: 'Total Rest',
        }], None),
    ('Tamox Total rCD4',
        drugs.ANY_ORDER, [{
            names.DRUG_CONDITION: 'Tamox',
            names.CELL_CONDITION: 'Total rCD4',
        }], None),
    ('Tamox rCD4',
        drugs.ANY_ORDER, [{
            names.DRUG_CONDITION: 'Tamox',
            names.CELL_CONDITION: 'rCD4',
        }], None),
    ('Total Resting +SAHA (335nM)',
        drugs.ANY_ORDER, [{
            names.DRUG_CONDITION: 'SAHA',
            names.CELL_CONDITION: 'Total Resting',
            names.CONC: '335',
            names.UNITS: 'nM'
        }], None),
    ('SAHA/HMBA 335nM/2.5mM 3hr',
        drugs.DRUG_SET, [{
            names.DRUG_CONDITION: 'SAHA',
            names.CONC: '335',
            names.UNITS: 'nM',
            names.DRUG_NOTE: '3hr'
        }, {
            names.DRUG_CONDITION: 'HMBA',
            names.CONC: '2.5',
            names.UNITS: 'mM',
            names.DRUG_NOTE: '3hr'
        }], None),
    ('PHA d5 8 12 15 19',
        drugs.MULTI_DAY, [{
            names.DRUG_CONDITION: 'PHA'
        },
            {names.DAY: '5'},
            {names.DAY: '8'},
            {names.DAY: '12'},
            {names.DAY: '15'},
            {names.DAY: '19'}
        ], None),
    ('PHA-Old 2 ug/ml Condition (Day 14)',
        drugs.ANY_ORDER, [{
            names.DRUG_CONDITION: 'PHA',
            names.CONC: '2',
            names.UNITS: 'ug/ml',
            names.DRUG_NOTE: 'Old',
            names.DAY: '14'
        }
        ], None),
    ('PHA Old (2 ug/ml) D14 D17',
        drugs.MULTI_DAY, [{
            names.DRUG_CONDITION: 'PHA',
            names.CONC: '2',
            names.UNITS: 'ug/ml',
            names.DRUG_NOTE: 'Old',
        },
            {names.DAY: '14'},
            {names.DAY: '17'}
        ], None),
    ('PHA + Ctrl (erb 38, 1ug/ml) d5 8 12 15 19',
        drugs.MULTI_DAY, [{
            names.DRUG_CONDITION: 'PHA'
        },
            {
            names.DRUG_CONDITION: 'Ctrl (erb 38,',
            names.CONC: '1',
            names.UNITS: 'ug/ml'
        },
            {names.DAY: '5'},
            {names.DAY: '8'},
            {names.DAY: '12'},
            {names.DAY: '15'},
            {names.DAY: '19'}
        ], None),
]


@pytest.mark.parametrize(
    'drug_condition, pattern, expected_matched, expected_unmatched',
    drug_conditions)
def test_value_matching(
    drug_condition,
    pattern,
    expected_matched,
    expected_unmatched
):
    matches = match(drug_condition, pattern)
    matched = matches['Matched']
    unmatched = matches['Unmatched']

    assert matched == expected_matched
    assert unmatched == expected_unmatched


def test_header_matching():
    header = '2.5'
    value = '0/1'
    expected = [{
        'Header Match': 'Dilution',
        'Positive': '0',
        'Total': '1',
        'Value Match': 'FULL'
    }]

    actual = list(process_cell(header, value))

    assert actual == expected


def test_day_header_matching():
    header = 'Day 21 in Culture'
    value = 'Day 21 in Culture'
    expected = [{
        'Header Match': 'Day',
        'Day': '21',
        'Value Match': 'FULL'
    }]

    actual = list(process_cell(header, value))

    assert actual == expected


def test_iupm_match():
    value = 'IUPM'
    matches = match(value, (iupms.IUPM,))
    unmatched = matches['Unmatched']

    assert not matches.get('Matched', None)
    assert not unmatched
