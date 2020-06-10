from app.helpers import names
from app.column import process_column


def process_headers(header_column):
    headers = [h.value for h in header_column]
    headers[0] = names.INFO
    return [
        {names.RAW: h, names.CLEAN: h.strip() if h else h}
        for h in headers
    ]


def process_sheet(ws, filename):
    pheresis = ws.title
    columns = list(ws.columns)

    headers = process_headers(columns[0])

    for num, column in enumerate(columns):
        yield from process_column(
            column,
            headers,
            pheresis,
            filename
        )
