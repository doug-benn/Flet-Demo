import pandas as pd

import flet as ft

DATA = None


def read_file(file_path):
    global DATA
    DATA = pd.read_csv(file_path)
    return DATA


def main(page: ft.Page):
    def reset_all(e):
        picker.disabled = False
        page.update()

    def button_clicked(e):
        selected_columns = []
        for checkbox in checkbox_list.controls:
            if not checkbox.value:
                selected_columns.append(checkbox.label)
        global DATA
        DATA = DATA.drop(selected_columns, axis=1)
        print(DATA)

    def generate_check_list(columns):
        for column in columns:
            checkbox_list.controls.append(ft.Checkbox(label=column, value=False))
        page.add(checkbox_list, submit_button)
        page.update()

    # Pick files dialog
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "Cancelled!"
        )
        if e.files:
            data = read_file(", ".join(map(lambda f: f.path, e.files)))
            columns = list(data)
            generate_check_list(columns)
        selected_files.update()
        picker.disabled = True
        page.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()
    checkbox_list = ft.ListView(height=300, expand=True, spacing=10)
    submit_button = ft.ElevatedButton(text="Submit", on_click=button_clicked)

    picker = ft.ElevatedButton(
        "Pick files",
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: pick_files_dialog.pick_files(
            allow_multiple=False, allowed_extensions=["csv"]
        ),
    )

    page.appbar = ft.AppBar(
        # leading_width=40,
        title=ft.Text("AppBar Example"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(ft.icons.RESTART_ALT, on_click=reset_all),
        ],
    )

    # hide all dialogs in overlay
    page.overlay.extend([pick_files_dialog])
    page.add(ft.Row([picker]), ft.Row([selected_files]))


ft.app(target=main)
