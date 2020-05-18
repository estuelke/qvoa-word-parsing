import pandas as pd
from datetime import datetime
from app.helpers.helpers import add_tables


# TODO: Update this method
def export_data(data):
    time = datetime.now()
    timestamp = time.strftime('%y%m%d_%H%M%S')
    output = f"output/qvoa_results_{timestamp}.xlsx"

    with pd.ExcelWriter(output) as writer:
        for (table, category, stage), df in data.items():
            if stage == 'Raw' and table != 'Check Data':
                continue
            if category == 'Meta Data':
                if 'Pheresis' in table:
                    df.to_excel(writer, sheet_name=table)
                else:
                    df.to_excel(writer, sheet_name=table, index=False)
                print(f"Table {table} exported")
            else:
                name = f"{category[0:4]}_{table[0:4]}_{stage[0:4]}" if stage != 'Raw' else f"{category[0:4]}_{table[0:4]}"
                df.to_excel(writer, sheet_name=name, index=False)
                print(f"Table {name} exported")

    add_tables(output)
    print('Finished')


def export_table(table, filename, columns=None, filter_rows=None):
    if filter_rows:
        table = table[filter_rows]

    if columns:
        table = table[columns]

    time = datetime.now()
    timestamp = time.strftime('%y%m%d_%H%M%S')
    output = f"{filename}_{timestamp}.xlsx"
