from app.helpers import names

IUPM = rf"""^
    (?P<{names.IUPM_MODIFIER}>\<|\>)?
    \s*
    (?P<{names.IUPM}>\d*\.\d+(?:e105|E\-05)?|N\/A|[\-]+|X)
    \s*
    \(?
    (?P<{names.IUPM_NOTE}>
        .old.|.new.|
        bad\scells\sdo\snot\suse|
        unreliable\sdue\sto\sprotocol\serror
    )?
    \)?
$"""

IUPM_TABLE_NOTE = rf"""^
    (?P<{names.TABLE_NOTE}>Old\sMethod\sIUPM)
$"""

PATTERNS = (IUPM, IUPM_TABLE_NOTE)
