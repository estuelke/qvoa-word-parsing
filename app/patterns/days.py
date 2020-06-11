from app.helpers import names
from app.patterns import drugs

DAY = rf"""^
    [Dd](?:ay\s+)?(?P<{names.DAY}>\d+(?:\/\d+)?)(?:\s+in\s+[Cc]ulture)?
    \s*\(?
        (?P<{names.DAY_NOTE}>GSK)?
    \)?
$"""

INITIAL = rf"""^
    (?P<{names.DAY_NOTE}>initial\sday\s(?P<{names.DAY}>\d+)\sELISA)
$"""

MULTI_DAYS = rf"""
    Day\s(?P<{names.DAY}>\d+)
    \s
    \(
        (?P<{names.DAY_NOTE}>PHA\sand\sreg\sIL-2|GSK,\sSAHA\sand\sCTRLS)
    \)
"""

DAY_WITH_EXP_NOTE = rf"""^
    Day\s(?P<{names.DAY}>\d+)\sin\s[Cc]ulture
    \s\*+
    (?P<{names.EXPERIMENT_NOTE}>one\smore.*?added\sat\sday\s\d+)
$"""

# DAY_WITH_INFO = (
#     rf"""^
#         \#
#         (?P<{names.PH_VERIFY}>\d+)\s # PH Number
#         (?P<{names.PH_DATE}>Nov\s05)\s # PH Date
#         (?P<{names.PID}>TC5006)\sSubject\s4\s # Patient ID (multiple)
#         (?P<{names.TIMEPOINT}>Week\s0b)\s # Study Timepoint
#         (?P<{names.STUDY_NAME}>Erad\sstudy)\s # Study Name
#         Day\s(?P<{names.DAY}>\d+)\sin\sculture
#     $""",
#     rf"""^
#         \#
#         (?P<{names.PH_VERIFY}>\d+)\s # PH Number
#         (?P<{names.PH_DATE}>Nov\s05)\s # PH Date
#         TC5006\s(?P<{names.PID}>Subject\s4)\s # Patient ID (multiple)
#         (?P<{names.TIMEPOINT}>Week\s0b)\s # Study Timepoint
#         (?P<{names.STUDY_NAME}>Erad\sstudy)\s # Study Name
#         Day\s(?P<{names.DAY}>\d+)\sin\sculture
#     $"""
# )

DAY_WITH_INFO = rf"""^
    \#
    (?P<{names.PH_VERIFY}>\d+)\s # PH Number
    (?P<{names.PH_DATE}>Nov\s05)\s # PH Date
    (?:(?P<{names.PID}>TC5006|Subject\s4)\s)+ # Patient ID (multiple)
    (?P<{names.TIMEPOINT}>Week\s0b)\s # Study Timepoint
    (?P<{names.STUDY_NAME}>Erad\sstudy)\s # Study Name
    Day\s(?P<{names.DAY}>\d+)\sin\sculture
$"""

PATTERNS = (
    DAY, INITIAL, MULTI_DAYS, DAY_WITH_EXP_NOTE, DAY_WITH_INFO,
    drugs.ANY_ORDER
)
