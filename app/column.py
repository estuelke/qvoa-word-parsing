import re
from app.cell import process_cell
from app.helpers import names


def get_initial_values(cell, pheresis, filename, header_info=None):
    coordinate = cell.coordinate
    header_info = header_info or {}
    raw_header = header_info.get(names.RAW, None)
    header = header_info.get(names.CLEAN, None)

    return {
        names.PH: pheresis,
        names.FILE: filename,
        names.CELL: coordinate,
        names.COL_ID: re.search(r'[A-Z]+', coordinate)[0],
        names.ROW_ID: re.search(r'\d+', coordinate)[0],
        names.RAW_HEADER: raw_header,
        names.HEADER: header,
        names.RAW_VALUE: cell.value.strip() if cell.value else None,
    }


def process_column(col, headers, pheresis, filename):
    for row, cell in enumerate(col):
        if not cell.value or not cell.value.strip():
            continue

        row_header = headers[row]
        initial_values = get_initial_values(
            cell, pheresis, filename, row_header
        )

        clean_header = row_header[names.CLEAN]
        cell_value = cell.value.strip()

        for result in process_cell(clean_header, cell_value):
            yield {
                **initial_values,
                **result
            }
