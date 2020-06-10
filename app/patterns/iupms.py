from app.helpers import names

IUPM = rf"""^
    (?P<{names.IUPM_MODIFIER}>\<|\>)?
    \s*
    (?P<{names.IUPM}>\d*\.\d+(?:e105|E\-05)?)
    \s*
    \(?
    (?P<{names.IUPM_NOTE}>
        .old.|.new.|
        bad\scells\sdo\snot\suse|
        unreliable\sdue\sto\sprotocol\serror
    )?
    \)?
$"""

DOUBLE_IUPM = rf"""
    (?P<{names.IUPM_MODIFIER}>\<|\>)?
    \s*
    (?P<{names.IUPM}>\d*\.\d+(?:x10\-5)?)\s?(?=[\(\)])
"""

DOUBLE_IUPM_2 = rf"""
    (?P<{names.IUPM}>\d*\.\d+)
    \s*
    (?P<{names.IUPM_NOTE}>all\sdata|std\.?\sIUPM)
"""

IUPM_TABLE_NOTE = rf"^(?P<{names.TABLE_NOTE}>Old\sMethod\sIUPM)$"

WELL = rf"^(?P<{names.POSITIVE}>\d+|i)\/(?P<{names.TOTAL}>\d+)$"

PATTERNS = (IUPM, IUPM_TABLE_NOTE, WELL, DOUBLE_IUPM, DOUBLE_IUPM_2)
