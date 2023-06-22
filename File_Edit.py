import pandas as pd

import flet as ft


def main(page: ft.Page):
    DATA = pd.read_csv("./config.txt")

    def updateOnTap(e):
        e.control.content.value = "Hello John"
        page.update()

    def headers(df: pd.DataFrame) -> list:
        return [ft.DataColumn(ft.Text(header)) for header in df.columns]

    def rows(df: pd.DataFrame) -> list:
        rows = []
        for index, row in df.iterrows():
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Row(
                                ft.TextField(value=row[header]),
                                show_edit_icon=True,
                                on_tap=updateOnTap,
                            )
                        )
                        for header in df.columns
                    ]
                )
            )
        return rows

    datatable = ft.DataTable(columns=headers(DATA), rows=rows(DATA))

    page.add(datatable)


ft.app(target=main)
