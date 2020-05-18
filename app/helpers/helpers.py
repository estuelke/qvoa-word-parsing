import pandas as pd
from app.helpers import names
from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo


def add_tables(filename):
    wb = load_workbook(filename)
    style = TableStyleInfo(
        name='TableStyleMedium5',
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False
    )
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        if len(list(ws.values)) == 0:
            continue

        table_name = sheet.replace(' ', '_')
        tab = Table(displayName=table_name, ref=ws.dimensions)
        tab.tableStyleInfo = style
        ws.add_table(tab)

        print(f"{sheet} table generated")

    wb.save(filename)


def create_dataframe(name, data):
    if name == names.PH_INFO:
        return {names.RAW: pd.DataFrame(data).set_index(names.PH)}
    else:
        return {names.RAW: pd.DataFrame(data)}


def merge_dicts(dicts):
    return {k: d[k] for d in dicts for k, v in d.items()}


def extend_data(data, cumulative_data):
    for name, items in data.items():
        cumulative_data[name].extend(items)
    return cumulative_data
