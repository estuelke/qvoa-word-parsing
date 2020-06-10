import pytest
from app.helpers import names
from app.cell import process_cell, process_values
from app.patterns import iupms


def test_process_cells_yield_when_no_header():
    cell = process_cell(None, 'test value')
    assert next(cell) == {
        names.HEADER_MATCH: 'NO HEADER',
        names.UNMATCHED: 'test value'
    }

    with pytest.raises(StopIteration):
        next(cell)


def test_process_cells_yield_when_no_header_match_found():
    cell = process_cell('Non-Existent Header', 'test value')
    assert next(cell) == {
        names.HEADER_MATCH: None,
        names.UNMATCHED: 'test value'
    }

    with pytest.raises(StopIteration):
        next(cell)


def test_process_cells_yield_when_header_found_but_no_value_found():
    cell = process_cell('IUPMs', 'test value')

    assert next(cell) == {
        names.HEADER_MATCH: 'IUPM',
        names.VALUE_MATCH: None,
        names.UNMATCHED: 'test value'
    }

    with pytest.raises(StopIteration):
        next(cell)


def test_process_values_when_value_is_throwaway_value():
    value = 'IUPM'
    header_name = names.IUPM
    patterns = (iupms.IUPM,)

    processed_value = process_values(value, patterns, header_name)
    result = next(processed_value)

    expected = {
        names.HEADER_MATCH: header_name,
        names.VALUE_MATCH: 'FULL',
        names.EXCLUDE: True,
        names.EXCLUDE_REASON: 'Value is not part of the data set'
    }

    assert result == expected
    with pytest.raises(StopIteration):
        next(processed_value)
