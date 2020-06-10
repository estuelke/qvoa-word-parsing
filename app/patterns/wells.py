from app.helpers import names


# Pattern Fragments
WELL_NOTES = '|'.join((
    r'(?:all\s?|\d\s?)?s?molds?(?:\scont\.?)?',
    r'bbrx',
    r'(?:\d|one|two|four|)\spossible\s(?:positi|\+)ve(?:\swells?)?',
    r'\d\swells\swere\scontaminated',
    r"""
        \+?
        (?:w\/o\s)?
        (?:(?:\d+|one)\s?)?
        (?:(?:values|all|(?:\+ve\s)?wells?)\s?)?
        (?:(?:on|at|close\sto|(?:j\s?ust\s)?over)\s?)
        cut[\-\s]*off
    """,
    r'splashed\sso\sreliable\sresult\sus',
    r'\d\/\d\snon-splashed',
    r'false\spositive,\snext\sto\sstandards\s\(splash\?\sdrip\?\)',
    r'value\sat\scutoff,\sbut\spositive\son\sD19',
    r'not\scounted',
    r'not\sthe\ssame\swell',
    r'questionable,\slots\sof\slow\spositives',
    r'\b\dM\b',
    r'\d\swells\swere\s(?:fungal\s)?(?:contaminated|moldy)'
))

P24_RESULTS = '|'.join((
    r'(?:(?:\d+[\s,]*)+pg\/ml(?:,\s)?)+',
    r'(?<=\()(?:0\.0\d{2}(?:[\&\s]+)?)+(?=\))',
    r'0\.026,\s0.023'
))

DILUTIONS = '|'.join((
    r'0\.25(?=\smillion\scells\/ml)',
    r'(?<=condition\sof\s)0\.041(?=\sNOT\s0\.025)',
))


# Full Patterns
DEFAULT_WELL = rf"""^
    (?=.*?(?:
        (?P<{names.POSITIVE}>\d+|i)
        \s?\/
        (?P<{names.TOTAL}>\d+)
    ))
    (?=.*?(?P<{names.WELL_NOTE}>{WELL_NOTES}))?
    (?=.*?(?P<{names.WELL_SYMBOL}>[\*\?]+))?
    (?=.*?(?P<{names.P24_RESULT}>{P24_RESULTS}))?
    (?=.*?(?P<{names.DILN}>{DILUTIONS}))?
    .+
$"""

WELL_NO_VALUE = rf"""^
    (?P<{names.WELL_NOTE}>[\?\-\*x]+(?:\s\(all\smold\))?|Mold|N\/?[AD])
$"""

MULTIPLE_DATA_SETS = rf"""
    (?=[^\(\s]*?
        (?:\b(?P<{names.POSITIVE}>\d+)\b\s?\/\b(?P<{names.TOTAL}>\d+)\b)
    )
    (?=.*?(?P<{names.WELL_NOTE}>{WELL_NOTES}))?
    [^\(\)\s]+?
"""

MULTIPLE_POSITIVES = (
    rf"""^
        (?P<{names.POSITIVE}>\d+)
        \sor\s\d+
        \/
        (?P<{names.TOTAL}>\d+)
    $""",
    rf"""^
        \d+
        \sor\s(?P<{names.POSITIVE}>\d+)
        \/
        (?P<{names.TOTAL}>\d+)
    $""",
)

TABLE_NOTE = rf"""^
    (?P<{names.TABLE_NOTE}>1rst\sELISA.*?ABOVE)
$"""

DILUTION_ONLY = rf"""^
    (?P<{names.DILN}>[15]|\d\.\d+)
$"""

DOUBLE_DILUTION = rf"""
    (?P<{names.DILN}>2\.5|1\.0)\s*(?=[\(\)])
"""

PATTERNS = (
    WELL_NO_VALUE,
    TABLE_NOTE,
    MULTIPLE_POSITIVES,
    DEFAULT_WELL,
    MULTIPLE_DATA_SETS,
    DILUTION_ONLY,
    DOUBLE_DILUTION,
)
