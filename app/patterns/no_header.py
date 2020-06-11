from app.helpers import names

CELLS = '|'.join((
    r'CD4\sResting\sCells',
    r'GD\sdepleted\sCD4\sRest',
    r'Resting\sCD4',
    r'\/δdepleted\sResting\sCD4'
))

NO_HEADER = rf"""^
    (?<{names.CELL_CONDITION}>{CELLS})|
    (?<{names.TABLE_NOTE}>Two-way\ssort.*?performed)
$"""

PATTERNS = (NO_HEADER,)
