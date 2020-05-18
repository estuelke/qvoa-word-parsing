import re
from app.helpers import names
from app.patterns.values import (
    CONDITION_PATTERNS, DAY_PATTERNS, INFO_PATTERNS, IUPM_PATTERNS,
    TABLE_NOTE_PATTERNS, WELL_PATTERNS
)

CONDITION = re.compile(r'.*?Million|cor|Dilution\s*\([Mm]illion\)')
DAY = re.compile(rf"""^
    (?:initial\s)?(?:\#3\sNov\s05\sTC5006.*?)?
    D(?:ay)?\s*\d+(?:\/\d+)?(.*?or\sDay\s\d+.*?)?(?:\sin\sculture)?
    .*?
$""", re.X | re.I)
DILUTION = re.compile(r'[15]|\d\.\d+')
IUPM = re.compile(r'^(?:Old\sMethod\s)?IUPMs?')
INFO = re.compile(rf'^{names.INFO}$|^\#19\sJuly\s06|^\#18\sJune\s06')
TABLE_NOTE = re.compile(rf"""
    ^{names.TABLE_NOTE}:|
    ^\*\sMold\sin\swell\s1\sof\s2\.5\sTDM\sNa.ve\sPHA|
    ^New\sMethod\sa\sla\sSilicano|
    ^THESE\sVALUES\sFELT\sUNRELIABLE|
    ^.new.\sUNC\smethod\sas\sper\sRFS|
    ^Old\sUTSW\smethods\s
""", re.X | re.I)

PATTERN_MAP = (
    {
        'name': names.CONDITION,
        'pattern': CONDITION,
        'value_patterns': CONDITION_PATTERNS,
    },
    {
        'name': names.DILN,
        'pattern': DILUTION,
        'value_patterns': WELL_PATTERNS,
    },
    {
        'name': names.DAY,
        'pattern': DAY,
        'value_patterns': DAY_PATTERNS,
    },
    {
        'name': names.IUPM,
        'pattern': IUPM,
        'value_patterns': IUPM_PATTERNS,
    },
    {
        'name': names.INFO,
        'pattern': INFO,
        'value_patterns': INFO_PATTERNS,
    },
    {
        'name': names.TABLE_NOTE,
        'pattern': TABLE_NOTE,
        'value_patterns': TABLE_NOTE_PATTERNS
    }
)
