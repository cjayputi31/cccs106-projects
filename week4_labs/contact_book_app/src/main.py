# main.py
import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact, open_delete_dialog

def main(page: ft.Page):
    page.title = "Contact Book"
    page.window_width = 400
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    db_conn = init_db()

    name_input = ft.TextField(
        label="Name",
        width=350,
        border_color=ft.Colors.BLACK
    )
    phone_input = ft.TextField(
        label="Phone",
        width=350,
        border_color=ft.Colors.BLACK
    )
    email_input = ft.TextField(
        label="Email",
        width=350,
        border_color=ft.Colors.BLACK
    )
    inputs = (name_input, phone_input, email_input)

    contacts_list_view = ft.ListView(expand=1, spacing=10, auto_scroll=True)

    search_input = ft.TextField(
        label="Search contacts...",
        width=350,
        border_color=ft.Colors.BLACK,
        on_change=lambda e: display_contacts(page, contacts_list_view, db_conn, e.control.value)
    )

    add_button = ft.ElevatedButton(
        text="Add Contact",
        on_click=lambda e: add_contact(page, inputs, contacts_list_view, db_conn)
    )

    def toggle_theme(e):
        is_dark = page.theme_mode == ft.ThemeMode.LIGHT
        page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        e.control.icon = ft.Icons.LIGHT_MODE if not is_dark else ft.Icons.DARK_MODE

        text_box_border_color = ft.Colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLACK
        for text_field in [name_input, phone_input, email_input, search_input]:
            text_field.border_color = text_box_border_color

        page.update()

    theme_button = ft.IconButton(
        icon=ft.Icons.DARK_MODE,
        on_click=toggle_theme
    )

    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Row(
                            [ft.Text("Contact Book", size=20, weight=ft.FontWeight.BOLD), theme_button],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Text("Enter Contact Details:", size=16, weight=ft.FontWeight.BOLD),
                        name_input,
                        phone_input,
                        email_input,
                        add_button,
                        ft.Divider(),
                        ft.Text("Contacts:", size=16, weight=ft.FontWeight.BOLD),
                        search_input,
                        contacts_list_view,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    display_contacts(page, contacts_list_view, db_conn)

    def handle_app_lifecycle(e):
        if e.data == ft.AppLifecycleState.DETACH:
            db_conn.close()

    page.on_app_lifecycle_state_change = handle_app_lifecycle

if __name__ == "__main__":
    ft.app(target=main)