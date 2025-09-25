# app_logic.py
import flet as ft
from database import update_contact_db, delete_contact_db, add_contact_db, get_all_contacts_db

def _show_snack(page, text, bgcolor=None):
    sb = ft.SnackBar(
        ft.Text(text),
        bgcolor=bgcolor or ft.colors.BLACK,
        open=True,
        duration=2000
    )
    page.snack_bar = sb
    page.update()

def display_contacts(page, contacts_list_view, db_conn, search_term=""):
    """Fetches and displays all contacts in the ListView."""
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn, search_term)
    for contact in contacts:
        contact_id, name, phone, email = contact
        # avatar initial
        initial = (name.strip()[0].upper() if name and name.strip() else "?")
        avatar = ft.CircleAvatar(content=ft.Text(initial, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                 bgcolor=ft.Colors.BLUE, radius=22)

        left_col = ft.Column(
            [
                ft.Row([avatar, ft.Column([ft.Text(name, size=16, weight=ft.FontWeight.BOLD)], tight=True)], alignment=ft.MainAxisAlignment.START, spacing=12),
                ft.Row([ft.Icon(ft.Icons.PHONE, size=16), ft.Text(phone or "-", size=12)], alignment=ft.MainAxisAlignment.START),
                ft.Row([ft.Icon(ft.Icons.EMAIL, size=16), ft.Text(email or "-", size=12)], alignment=ft.MainAxisAlignment.START),
            ],
            tight=True
        )

        menu = ft.PopupMenuButton(
            icon=ft.Icons.MORE_VERT,
            items=[
                ft.PopupMenuItem(
                    text="Edit",
                    icon=ft.Icons.EDIT,
                    on_click=lambda _, c=contact: open_edit_dialog(page, c, db_conn, contacts_list_view)
                ),
                ft.PopupMenuItem(),
                ft.PopupMenuItem(
                    text="Delete",
                    icon=ft.Icons.DELETE,
                    on_click=lambda _, cid=contact_id: confirm_delete(page, cid, db_conn, contacts_list_view)
                ),
            ],
        )

        card = ft.Card(
            content=ft.Container(
                padding=12,
                content=ft.Row([left_col, menu], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ),
            elevation=2,
            margin=ft.margin.symmetric(vertical=6, horizontal=8),
            shape=ft.RoundedRectangleBorder(radius=8)
        )
        contacts_list_view.controls.append(card)

    page.update()

def add_contact(page, inputs, contacts_list_view, db_conn, search_field):
    """Adds a new contact and refreshes the list with validation and duplicate check."""
    name_input, phone_input, email_input = inputs
    valid = True

    # Validation
    if not name_input.value or not name_input.value.strip():
        name_input.error_text = "Name required"
        valid = False
    else:
        name_input.error_text = None

    if not phone_input.value or not phone_input.value.strip():
        phone_input.error_text = "Phone required"
        valid = False
    else:
        phone_input.error_text = None

    if not email_input.value or not email_input.value.strip():
        email_input.error_text = "Email required"
        valid = False
    else:
        email_input.error_text = None

    if not valid:
        page.update()
        return

    # attempt to insert; add_contact_db returns False if duplicate
    inserted = add_contact_db(db_conn, name_input.value.strip(), phone_input.value.strip(), email_input.value.strip())
    if not inserted:
        name_input.error_text = "Contact name already exists"
        page.update()
        return

    # clear fields
    for field in inputs:
        field.value = ""
        field.error_text = None

    # show success snackbar
    _show_snack(page, "Contact added", bgcolor=ft.Colors.GREEN)

    display_contacts(page, contacts_list_view, db_conn, search_field.value)
    page.update()

def delete_contact(page, contact_id, db_conn, contacts_list_view, search_term=""):
    """Deletes a contact and refreshes the list."""
    delete_contact_db(db_conn, contact_id)
    _show_snack(page, "Contact deleted", bgcolor=ft.Colors.ORANGE)
    display_contacts(page, contacts_list_view, db_conn, search_term)

def confirm_delete(page, contact_id, db_conn, contacts_list_view):
    """Asks for confirmation before deleting a contact."""
    def yes_action(e):
        delete_contact(page, contact_id, db_conn, contacts_list_view)
        dialog.open = False
        page.update()
    def no_action(e):
        dialog.open = False
        page.update()
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Delete"),
        content=ft.Text("Are you sure you want to delete this contact?"),
        actions=[
            ft.TextButton("No", on_click=no_action),
            ft.TextButton(
                content=ft.Text("Yes", color=ft.Colors.RED),
                on_click=yes_action
            ),
        ],
    )
    page.open(dialog)

def open_edit_dialog(page, contact, db_conn, contacts_list_view):
    """Opens a dialog to edit a contact's details with validation and duplicate-name handling."""
    contact_id, name, phone, email = contact
    edit_name = ft.TextField(label="Name", value=name, width=320)
    edit_phone = ft.TextField(label="Phone", value=phone, width=320)
    edit_email = ft.TextField(label="Email", value=email, width=320)

    # Apply colors based on theme
    def apply_edit_colors():
        fields = [edit_name, edit_phone, edit_email]
        if page.theme_mode == ft.ThemeMode.DARK:
            for f in fields:
                f.color = ft.Colors.WHITE
                f.border_color = ft.Colors.WHITE
        else:
            for f in fields:
                f.color = ft.Colors.BLACK
                f.border_color = ft.Colors.BLACK
    apply_edit_colors()

    def save_and_close(e):
        if not edit_name.value.strip():
            edit_name.error_text = "Name cannot be empty"
            page.update()
            return
        edit_name.error_text = None

        success = update_contact_db(db_conn, contact_id, edit_name.value.strip(), edit_phone.value.strip(), edit_email.value.strip())
        if not success:
            edit_name.error_text = "Another contact with this name exists"
            page.update()
            return

        dialog.open = False
        _show_snack(page, "Contact updated", bgcolor=ft.Colors.GREEN)
        page.update()
        display_contacts(page, contacts_list_view, db_conn)

    dialog_content = ft.Container(
        content=ft.Column([edit_name, edit_phone, edit_email], tight=True),
        padding=16,
        width=420
    )

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Contact"),
        content=dialog_content,
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False) or page.update()),
            ft.TextButton("Save", on_click=save_and_close),
        ]
    )

    page.open(dialog)
