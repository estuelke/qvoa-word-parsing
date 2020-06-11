import regex as re
from app.helpers import names
from app.patterns import conditions, days, drugs, info, iupms, no_header, wells


def compile_patterns(patterns):
    compiled = []
    for pattern in patterns:
        if isinstance(pattern, tuple):
            compiled.append(
                tuple(re.compile(p, re.X | re.I) for p in pattern)
            )
        else:
            compiled.append(re.compile(pattern, re.X | re.I))

    return tuple(compiled)


# Pattern Sets
CONDITION_PATTERNS = (
    *compile_patterns(conditions.PATTERNS),
    *compile_patterns(drugs.PATTERNS)
)

DAY_PATTERNS = compile_patterns(days.PATTERNS)

INFO_PATTERNS = compile_patterns(info.PATTERNS)

IUPM_PATTERNS = compile_patterns(iupms.PATTERNS)

TABLE_NOTE_PATTERNS = compile_patterns((
    rf"""^
        (?:{names.TABLE_NOTE}:\s*)?(?P<{names.TABLE_NOTE}>.*)
    $""",
))

WELL_PATTERNS = compile_patterns(wells.PATTERNS)

NO_HEADER_PATTERNS = (
    *compile_patterns(no_header.PATTERNS),
    *WELL_PATTERNS,
    *IUPM_PATTERNS,
    *DAY_PATTERNS,
    *CONDITION_PATTERNS,
)
