# app_logic.py
import flet as ft
from database import update_contact_db, delete_contact_db, add_contact_db, get_all_contacts_db


def display_contacts(page, contacts_list_view, db_conn, search_term: str = ""):
    """Fetches and displays all contacts in the ListView, with optional filtering."""
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn, search_term)
    for contact in contacts:
        contact_id, name, phone, email = contact
        contacts_list_view.controls.append(
            ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Column(
                        controls=[
                            ft.ListTile(
                                title=ft.Text(name, size=18, weight="bold"),
                                trailing=ft.PopupMenuButton(
                                    icon=ft.Icons.MORE_VERT,
                                    items=[
                                        ft.PopupMenuItem(
                                            text="Edit",
                                            icon=ft.Icons.EDIT,
                                            on_click=lambda e, c=contact: open_edit_dialog(
                                                page, c, db_conn, contacts_list_view
                                            ),
                                        ),
                                        ft.PopupMenuItem(),  # divider
                                        ft.PopupMenuItem(
                                            text="Delete",
                                            icon=ft.Icons.DELETE,
                                            on_click=lambda e, cid=contact_id: open_delete_dialog(
                                                page, cid, db_conn, contacts_list_view
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.PHONE, size=16),
                                    ft.Text(phone or "N/A"),
                                ],
                                spacing=5,
                            ),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.EMAIL, size=16),
                                    ft.Text(email or "N/A"),
                                ],
                                spacing=5,
                            ),
                        ]
                    ),
                ),
            )
        )
    page.update()


def add_contact(page, inputs, contacts_list_view, db_conn):
    """Adds a new contact and refreshes the list, with validation."""
    name_input, phone_input, email_input = inputs

    # Clear previous error messages
    name_input.error_text = None
    phone_input.error_text = None
    email_input.error_text = None

    has_error = False

    if not name_input.value.strip():
        name_input.error_text = "Name cannot be empty"
        has_error = True

    if not phone_input.value.strip():
        phone_input.error_text = "Phone should not be empty"
        has_error = True

    if not email_input.value.strip():
        email_input.error_text = "Email should not be empty"
        has_error = True

    if has_error:
        page.update()
        return

    add_contact_db(
        db_conn,
        name_input.value.strip(),
        phone_input.value.strip(),
        email_input.value.strip(),
    )
    for field in inputs:
        field.value = ""
    display_contacts(page, contacts_list_view, db_conn)
    page.update()


def delete_contact(page, contact_id, db_conn, contacts_list_view):
    """Deletes a contact and refreshes the list."""
    delete_contact_db(db_conn, contact_id)
    display_contacts(page, contacts_list_view, db_conn)
    page.update()


def open_delete_dialog(page, contact_id, db_conn, contacts_list_view):
    """Opens a confirmation dialog for deleting a contact."""

    def confirm_delete(e):
        delete_contact(page, contact_id, db_conn, contacts_list_view)
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Deletion"),
        content=ft.Text("Are you sure you want to delete this contact?"),
        actions=[
            ft.TextButton(
                "No", on_click=lambda e: (setattr(dialog, "open", False), page.update())
            ),
            ft.TextButton("Yes", on_click=confirm_delete),
        ],
    )
    page.dialog = dialog
    dialog.open = True
    page.update()


def open_edit_dialog(page, contact, db_conn, contacts_list_view):
    """Opens a dialog to edit a contact's details."""
    contact_id, old_name, old_phone, old_email = contact

    name_input = ft.TextField(
        label="Name",
        value=old_name,
        width=300,
        border_color=ft.Colors.BLACK
        if page.theme_mode == ft.ThemeMode.LIGHT
        else ft.Colors.WHITE,
    )
    phone_input = ft.TextField(
        label="Phone",
        value=old_phone,
        width=300,
        border_color=ft.Colors.BLACK
        if page.theme_mode == ft.ThemeMode.LIGHT
        else ft.Colors.WHITE,
    )
    email_input = ft.TextField(
        label="Email",
        value=old_email,
        width=300,
        border_color=ft.Colors.BLACK
        if page.theme_mode == ft.ThemeMode.LIGHT
        else ft.Colors.WHITE,
    )

    def update_contact(e):
        if not name_input.value.strip():
            name_input.error_text = "Name cannot be empty"
            page.update()
            return

        update_contact_db(
            db_conn,
            contact_id,
            name_input.value.strip(),
            phone_input.value.strip(),
            email_input.value.strip(),
        )

        dialog.open = False
        page.update()

        display_contacts(page, contacts_list_view, db_conn)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Contact"),
        content=ft.Column(
            [name_input, phone_input, email_input],
            tight=True,
        ),
        actions=[
            ft.TextButton(
                "Cancel",
                on_click=lambda e: (setattr(dialog, "open", False), page.update()),
            ),
            ft.ElevatedButton("Save", on_click=update_contact),
        ],
    )
    page.dialog = dialog
    dialog.open = True
    page.update()
