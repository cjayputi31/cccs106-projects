# main.py
import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact

def main(page: ft.Page):
    page.title = "Contact Book"
    page.window_width = 480
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.LIGHT

    db_conn = init_db()

    name_input = ft.TextField(label="Name", width=360, hint_text="Full name")
    phone_input = ft.TextField(label="Phone", width=360, hint_text="09xx-xxx-xxxx")
    email_input = ft.TextField(label="Email", width=360, hint_text="name@example.com")
    search_field = ft.TextField(
        label="Search",
        width=360,
        prefix=ft.Icon(ft.Icons.SEARCH),
        on_change=lambda e: display_contacts(page, contacts_list_view, db_conn, search_field.value)
    )
    inputs = (name_input, phone_input, email_input)

    contacts_list_view = ft.ListView(expand=True, spacing=6, auto_scroll=False)
    # Buttons 
    add_button = ft.FilledButton(
        "Add Contact",
        icon=ft.Icons.PERSON_ADD,
        on_click=lambda e: add_contact(page, inputs, contacts_list_view, db_conn, search_field)
    )

    theme_toggle = ft.IconButton(icon=ft.Icons.DARK_MODE, tooltip="Toggle Theme")
    def apply_textfield_style():
        color = ft.Colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLACK
        for field in [name_input, phone_input, email_input, search_field]:
            field.border_color = color
            field.color = color

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_toggle.icon = ft.Icons.WB_SUNNY
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_toggle.icon = ft.Icons.DARK_MODE
        apply_textfield_style()
        page.update()

    theme_toggle.on_click = toggle_theme

    header = ft.Row(
        [
            ft.Text("Contact Book", size=24, weight=ft.FontWeight.BOLD),
            theme_toggle
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    form_card = ft.Card(
        content=ft.Container(
            padding=16,
            content=ft.Column(
                [
                    ft.Text("New Contact", size=16, weight=ft.FontWeight.W_600),
                    ft.Row([name_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([phone_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([email_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([add_button], alignment=ft.MainAxisAlignment.END),
                ],
                tight=True,
                spacing=8
            )
        ),
        elevation=3,
        margin=ft.margin.symmetric(vertical=8, horizontal=12),
        shape=ft.RoundedRectangleBorder(radius=10)
    )

    contact_section = ft.Column(
        [
            ft.Text("Contacts", size=16, weight=ft.FontWeight.W_600),
            search_field,
            ft.Container(content=contacts_list_view, expand=True)
        ],
        expand=True,
        spacing=8
    )

    page.add(
        ft.Column(
            [
                header,
                ft.Divider(thickness=1),
                form_card,
                ft.Divider(thickness=1),
                contact_section
            ],
            expand=True,
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        )
    )

    apply_textfield_style()
    display_contacts(page, contacts_list_view, db_conn)

if __name__ == "__main__":
    ft.app(target=main)
