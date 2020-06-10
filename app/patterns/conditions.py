from app.helpers import names

CONDITION_SYMBOLS = '|'.join((r'\*+',))

MOUSE = rf"""^
    (?P<{names.SAMPLE_ID}>BM?\s?\d+|Mouse\s\d{{3}}\-\d)
    (?:\s*\(?(?P<{names.SOURCE_NOTES}>.*?)\)?)?
$"""

MULLINS = rf"""^
    (?P<{names.SAMPLE_ID}>(JM|Mullins)\s*\d+)
    \s*(?:cells|\(Mullins\))?\s*
    (?P<{names.DRUG_CONDITION}>PHA)?
$"""

SOUTH_AFRICA = rf"""^
    (?P<{names.SAMPLE_ID}>(RS\-)?SA\s*\d+)
    (?:\s\((?P<{names.DILN}>0\.3)e6\/ml\)?)?
$"""

PATTERNS = (
    MOUSE,
    MULLINS,
    SOUTH_AFRICA
)
