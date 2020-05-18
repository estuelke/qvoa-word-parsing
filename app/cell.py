from app.helpers import names
from app.patterns.headers import PATTERN_MAP
from app.match import match, header_match


def process_values(cell_value, value_patterns, header_name):
    if not cell_value:
        return

    for pattern in value_patterns:
        matched_data = match(cell_value, pattern)

        matches = matched_data.get(names.MATCHED, [])
        unmatched = matched_data[names.UNMATCHED]

        if unmatched:
            match_info = {
                names.HEADER_MATCH: header_name,
                names.UNMATCHED: unmatched,
                names.VALUE_MATCH: 'PARTIAL'
            }
        else:
            match_info = {
                names.HEADER_MATCH: header_name,
                names.VALUE_MATCH: 'FULL'
            }

        if not matches and not unmatched:
            yield {
                **match_info,
                names.EXCLUDE: True,
                names.EXCLUDE_REASON: 'Value is not part of the data set'
            }

        for m in matches:
            yield {**m, **match_info}

        if not unmatched:
            break
    else:
        yield {
            names.HEADER_MATCH: header_name,
            names.VALUE_MATCH: None,
            names.UNMATCHED: cell_value
        }


def process_cell(header, cell_value):
    if not header:
        # TODO: Process headerless cell
        yield {names.HEADER_MATCH: 'NO HEADER', names.UNMATCHED: cell_value}
        return

    for header_state in PATTERN_MAP:
        header_pattern = header_state['pattern']

        if header_match(header, header_pattern):
            value_patterns = header_state['value_patterns']
            header_name = header_state['name']

            yield from process_values(
                cell_value,
                value_patterns,
                header_name
            )

            break
    else:
        # All headers should be matched and this code should not execute
        # Leaving in as it was used to help with processing and may
        #   help with future scripts of this nature
        yield {names.HEADER_MATCH: None, names.UNMATCHED: cell_value}
