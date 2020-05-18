import re
from app.helpers import names
from app.patterns import conditions, drugs, info, iupms, wells


def compile_patterns(patterns):
    compiled = []
    for pattern in patterns:
        if isinstance(pattern, tuple):
            compiled.append(
                tuple(re.compile(p, re.X | re.I) for p in pattern)
            )
        else:
            compiled.append(re.compile(pattern, re.X | re.X))

    return tuple(compiled)


# Pattern Sets
CONDITION_PATTERNS = (
    *compile_patterns(conditions.PATTERNS),
    *compile_patterns(drugs.PATTERNS)
)

DAY_PATTERNS = compile_patterns((
    r'[Dd]ay\s+(?P<Day>\d+)\s+in\s+[Cc]ulture',
))

INFO_PATTERNS = compile_patterns(info.PATTERNS)

IUPM_PATTERNS = compile_patterns(iupms.PATTERNS)

TABLE_NOTE_PATTERNS = compile_patterns((
    rf"""^
        {names.TABLE_NOTE}:\s*(?P<note>.*)
    $""",
))

WELL_PATTERNS = compile_patterns(wells.PATTERNS)
