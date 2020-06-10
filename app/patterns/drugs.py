from app.helpers import names
from app.patterns.conditions import CONDITION_SYMBOLS


# Pattern Variables
DRUGS = '|'.join((
    r'669(?=\+)',
    r'^669$',
    r'^[ABC]$',
    r"""
        (?<=Mrk\s10\s\(\d{3}nM\)\s\+\s)13|
        (?<=Mrk\s10\s\+\s)13|
        (?<=Mrk\s10\+)13|
        (?<=Mrk10\s\+)13|
        13(?=\s\(\d{3}nm\))
    """,
    r'ALT(?:\s*\d+)?',
    r'Bromo(?:sporin)?',
    r'B[RY]{2}O',
    r'BTX\sLuci',
    r'C7A',
    r'cMyc(?:\sCtrl)?',
    r'Disulf(?:iram)?',
    r'DZNEP(?:\s\d+)?',
    r'Entinostat',
    r'ETS',
    r'EZH2(?:\ssi\s?RNA)?',
    r'FH535\s+B\-cat(?:\s+inhib)?',
    r'Gilead[\-\s]+A',
    r'GSK[\s\-]*(?:Ing\s*)?(?:826|445|463|343)A?',
    r'GSK(?:-ING(enol)?)?(?!\sCTRL)',
    r'(?:(?:BTX|Lonza|T\d?)\s?)?HDAC\s?[\di](?:\ssi\s?RNA|\s3308)?|3308',
    r'(?<!No\s)IL-?(?:2|15)(?:\-B\b)?',
    r'IL-?7(?=$)',
    r'IL-?7(?=\s\()',
    r'\bIng(?:(?:enol(?:\sDB)?)|(?:[\s-]DB)|(?:\s*445A?)|\b)',
    r'IONO',
    r'J(?:NG|A)(?:611|508)',
    r'JNJ(?:\s*(?:\d+)|(?:\s*[-–]fu(?:rin)?))?',
    r'JQ\-?1',
    r'(?<!MRK\s)L\s*\d{3}',
    r'L\-412',
    r'LN?FN?B',
    r'LY(?:-B)?',
    r'(?:(?:BTX|Lonza|Neon|T\d)\s)?Luci(?:ferase)?(?:\ssiRNA)?',
    r'(?<!J)M17(?!95)',
    r'Medi(?:a|um)',
    r'\bMe?R?c?K[\s\-]*L?\s*\d+\b',
    r'MOO1',
    r'Na\s*Crot',
    r'PamSK',
    r'Pano?(?:binostat?)?',
    r"""
        PHA([-\s][ABM]\b)?(?:\s*control)?
    """,
    r'PMA',
    r'PROST',
    r'Romi(?:depsin)?',
    r'SAHA(?:\-Selch)?',
    r'Suv39(?:\ssiRNA)?',
    r'Tamox(?:iphen)?',
    r'TNFα',
    r"""
        (?:C(?:on)?tro?l\s+)?
        (?:Toxin)?
        [\s\(]+
        (?:3b3-?)?
        (?:erb\s*)?
        (?:PE?)?38
        [,\)]
    """,
    r'(?:Control\s+)?Toxin[\s\(]+(?:3b3-?)?(?:erb)?PE?38[,\)]',
    r'U(?:NC\s*)?(?:669|63[89]|1105)',
    r'Drug\s+[A-Z]',
    '6-Thio', 'AZD', 'CD27L', 'DMSO',
    'GSK', 'HMBA', 'HMBPP', 'iBET', 'IDT', 'ITD', 'PF1', 'VPA',
))
DAY = rf"""
    \bD(?:ay)?
    [\s-]*
    (?!0)
    (?P<{names.DAY}>\d+|\?)
"""
CONCENTRATIONS = '|'.join((
    r'(?:\d+(?:\.\d+)?)|(?:\.\d+)',
    r'x+(?=%)',
    r'x+(?=\s[nm]M)',
    r'(?=%)',
    r"""
        (?<=[\s\(\-])
        (?:(?:0\.)?335|250|0\.00[35]|0\.010)
        (?:(?=[\)n\+])|$)
    """,
    r'(?=nm)',
))
UNITS = '|'.join((
    r'[mnuµg][gm]?[\/\\]ml',
    r'[mnuµ][Mg]0?',
    r'(?<=\d)U\b',
    r'(?<=(?:335|250))n?(?:(?=[\)\+])|$)',
    r'(?<=(?:0\.335|0\.00[35]|0\.010))%?',
    r'%',
))
DRUG_NOTES = '|'.join((
    r'3day',
    r'(?:24|48)\s*(?:well|h(?:ou)?r?s?)',
    r'(?:\d+\s*hrs?[\s/]*(?:pulse)?)+',
    r'Compressed\s*Protocol',
    r'Conc\.',
    r'Delayed',
    r'equivalent\s+Vol\s+used\s+in\s+UNC\s+638\s+expmts',
    r'(?-i:EXP)\s*\d*',
    r'GSK\sCTRL',
    r'Int\.\s+Inh\.\s+day\s+0\-3',
    r'new\s+std\.',
    r'No\s*IL\-?2',
    r'No\spellets\sfor\sDay\s15',
    r'non\-splashed\s+wells',
    r'(?<=\-|\s)Old\b',
    r'pulsed\s+for\s+4\s+hr(?:\s+with\s+HMBA\s+followed\s+by\s+SAHA)?',
    r'Regular(?!\srest)',
    r'Short(?:\s*exposure)?(?:\s*\d*\s*hrs)?',
    r'(?<=Bromo\s)Sup',
    r'SitOut',
    r'splashed',
    r'Transf',
    r'washed',
    r'with\s+splashes',
    'Bulk', 'Daniel', 'Old', 'Simoa', 'Transwell',
))
FEEDERS = '|'.join((
    r'Donor(?:\s*\D+)?',
    r'molt4?s?([\/\-]ccr5)?',
    r'(?<=IL-2\s)Sup(?=\s5U)',
    r'(?<=PHA\s\+\s)sup$',
    r'Supt1(?:HUR5)?',
    'Buffy',
))

METHODS = '|'.join((r'\(?E(?:Z|asy)Sep\)?', r'\bES\b'))
ANTIRETROVIRALS = '|'.join((
    r"""
        (?:without\s+)?
        RT(?:[\s\+\-–]+|\s+and\s+)Int\.?\s+Inh(?:ib)?\.?|
        \bRT\b|
        \bInt\.?\s+Inh(?:ib)?\.?\b
    """,
    r'Rx',
))

SOURCE_NOTES = '|'.join((
    r'IL-7\s*31?2(?:10|06)\s(?:WK44|Day\s0)',
))

CELLS = '|'.join((
    r'\/\sT-cells',
    r'\(?cell\spellets?\)?',
    r'Dendritic',
    r'(?:γ?\/?δ|g\/d)\s*(?:[\/-]*depleted[\-\s]*(?:rest(?:ing|\s+CD4\+)?)?)?',
    r'\bGD\b',
    r'CD25\snegative',
    r'CD27\-\sAll',
    r'CD3\/CD28',
    r'(?:(?:CD)?(?:27|45)[\s\+\-]*)?RA[\+\-](?:\s\(tn\s\+\sttd\))?|CD27\+?',
    r'ISO[12](?:,?\sCD27\+\sRA[\+\-]|\sELU2)',
    r'Mock(?:\sTransf)?',
    r'nonCD4\sor\sactCD4',
    r'(?<!\+\s)Sup$',
    r"""
        (?:
            (?:
                (?:
                    Total|
                    Reg(?:ular)?|
                    \/[\s\-]*depleted[\-\s]*
                )
                \s*
            )?
            (?:
                (?:Rest(?:ing)?(?:\s*r?CD4(?!5)\+?)?)|
                (?:r?(?<!non|act)CD4(?!5)\+?)
            )
        )|
        \/[\s\-]*depleted
    """,
    r'T[DE]M\s*NA[Ïi]VE',
    r'(?!<T[DE]M\s)NA[Ïi]VE(?:[\s\/]+TDM)?',
    r'T[CDEST]{1,2}M(?:\/T[CT]M)?',
    r'T\sregs\sCD25\shi',
    r'VD\d',
    r'VCTR\sTRANSF',
))

CELL_NOTES = '|'.join((
    r'1:1\s(?:cell:bead|ratio)',
    r'Beads',
    r'central\s*\+\s*transitional',
    r'effecto?r',
    r'Mock\sTransf\sexperiment\sby\sKK',
    r'na[ïi]ve\s\+\std',
    r'RA\snot\sdepleted',
    r'Sort(?:ed)?(?:\s*by\s*size,\s*not\s*pure)?',
    r'(?<=\()Tem(?=\))',
    r'(?<=\()Tcm\s\+\sTtm(?=\))'
))


# Overall Format of Drug Condition for drugs in any order
DRUG_FORMAT = r"""
    (?:
        [^\/\+]|
        #  Forward Slash Exceptions
        (?<=[gumt])\/(?=[dmt])|
        \/(?=ccr5)|
        \/(?=depleted)|
        \/(?=\sdepleted)|
        \/(?=\-depleted)|
        \/(?=\-\sdepleted)|
        (?<=Molt)\/|
        # Plus Sign Exceptions
        (?<=central)\+(?=\stransitional)|
        (?<=effector\)\s)\+(?=\sSAHA)|
        (?<=IL2)\+(?=\s\(naïve)|
        (?<=PHA)\+(?=\s\(central)|
        (?<=PHA)\+(?=\s\(effector)|
        (?<=PHA)\+(?=\s\(naïve)|
        (?<=PHA\s)\+(?=sup$)|
        (?<=\bResting\s)\+(?=SAHA)|
        (?<=\bnaïve\s)\+(?=\std\b)|
        (?<=transitional\)\s)\+(?=\sSAHA)|
        (?<=\bcd27)\+|
        (?<=cd4)\+|
        (?<=\bRA)\+|
        (?<=\bRA\+\s)\+|
        (?<=\bRA\-\s)\+|
        \+(?=\sMOLT)|
        \+(?=\sR[xT]\b)|
        \+(?=\ssup)|
        \+(?=\sInt\sInh)
    )
"""

DRUG_CONCENTRATION_UNITS = rf"""
    (?P<{names.CONC}>{CONCENTRATIONS})
    (?:\s*
        (?P<{names.UNITS}>{UNITS})
    )
"""

# Full Patterns
ANY_ORDER = rf"""
    (?={DRUG_FORMAT}*?(?P<{names.DRUG_CONDITION}>{DRUGS}))
    (?={DRUG_FORMAT}*?{DRUG_CONCENTRATION_UNITS})?
    (?={DRUG_FORMAT}*?(?P<{names.METHOD}>{METHODS}))?
    (?={DRUG_FORMAT}*?(?P<{names.CELL_CONDITION}>{CELLS}))?
    (?={DRUG_FORMAT}*?(?P<{names.CELL_NOTES}>{CELL_NOTES}))?
    (?={DRUG_FORMAT}*?(?P<{names.FEEDERS}>{FEEDERS}))?
    (?={DRUG_FORMAT}*?(?P<{names.DRUG_NOTE}>{DRUG_NOTES}))?
    (?={DRUG_FORMAT}*?(?P<{names.CONDITION_SYMBOL}>{CONDITION_SYMBOLS}))?
    (?={DRUG_FORMAT}*?(?P<{names.ANTIRETROVIRALS}>{ANTIRETROVIRALS}))?
    (?={DRUG_FORMAT}*?(?P<{names.SOURCE_NOTES}>{SOURCE_NOTES}))?
    (?={DRUG_FORMAT}*?{DAY})?
    {DRUG_FORMAT}+
"""


def drug_set_template(drug1, drug2, conc1, conc2):
    return rf"""^
        {drug1}
        \s?[\/\+]\s?
        {drug2}
        \s?[\(]?
        {conc1}
        \s?[\/,\+]\s?
        {conc2}
        [\)]?
        (?:
            [\s]
            (?P<{names.DRUG_NOTE}>3hr)
        )?
    $"""


DRUG_SET = (
    drug_set_template(
        rf"(?P<{names.DRUG_CONDITION}>{DRUGS})",
        rf"(?:{DRUGS})",
        rf"{DRUG_CONCENTRATION_UNITS}",
        rf"(?:{CONCENTRATIONS})[\s]*(?:{UNITS})"
    ),
    drug_set_template(
        rf"(?:{DRUGS})",
        rf"(?P<{names.DRUG_CONDITION}>{DRUGS})",
        rf"(?:{CONCENTRATIONS})[\s]*(?:{UNITS})",
        rf"{DRUG_CONCENTRATION_UNITS}"
    )
)

ONE_CONC_FOR_EACH = (
    rf"""^
        (?P<{names.DRUG_CONDITION}>Mrk\s10)
        \s\+\s13\s
        (?P<{names.CONC}>200)
        \s
        (?P<{names.UNITS}>nM)
        \seach
    $""",
    rf"""^
        Mrk\s10\s\+\s
        (?P<{names.DRUG_CONDITION}>13)
        \s
        (?P<{names.CONC}>200)
        \s
        (?P<{names.UNITS}>nM)
        \seach
    $"""
)

MULTI_DAY = (
    rf"""
        (?=[^\+]*?(?P<{names.DRUG_CONDITION}>{DRUGS}))
        (?=[^\+]*?(?P<{names.DRUG_NOTE}>{DRUG_NOTES}))?
        (?=[^\+]*?(?:\sCondition))?
        (?=[^\+]*?(?:{DRUG_CONCENTRATION_UNITS}))?
        [^\+]+
    """,
    rf"""
        (?P<{names.DAY}>
            (?<!3)[1]?[245789]
        )
    """
)

CELLS_ONLY = rf"""^
    (?=.*?(?P<{names.CELL_CONDITION}>{CELLS}))
    (?=.*?{DRUG_CONCENTRATION_UNITS})?
    (?=.*?(?P<{names.DRUG_NOTE}>{DRUG_NOTES}))?
    (?=.*?(?P<{names.CELL_NOTES}>{CELL_NOTES}))?
    (?=.*?(?P<{names.CONDITION_SYMBOL}>{CONDITION_SYMBOLS}))?
    (?=.*?{DAY})?
    .+
$"""

NOTES_ONLY = rf"""^
    (?P<{names.SOURCE_NOTES}>{SOURCE_NOTES})|
    (?P<{names.DRUG_NOTE}>{DRUG_NOTES})(?:\-(?P<{names.FEEDERS}>Buffy))?|
    (?P<{names.CELL_NOTES}>{CELL_NOTES})
$"""

CONCENTRATION_ONLY = rf"^\({DRUG_CONCENTRATION_UNITS}\)$"

PATTERNS = (
    CONCENTRATION_ONLY,
    NOTES_ONLY,
    ONE_CONC_FOR_EACH,
    DRUG_SET,
    CELLS_ONLY,
    ANY_ORDER,
    MULTI_DAY,
)
