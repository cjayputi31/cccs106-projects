import flet as ft
from db_connection import connect_db
from mysql.connector import Error

def main(page: ft.Page):
    # Configure the page
    page.window.alignment = ft.alignment.center
    page.window.frameless = True
    page.title = "User Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.height = 350
    page.window.width = 400
    page.bgcolor = ft.Colors.AMBER_ACCENT
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    # UI Controls
    login_title = ft.Text(
        "User Login",
        size=20,
        weight=ft.FontWeight.BOLD,
        font_family="Arial",
        text_align=ft.TextAlign.CENTER,
    )

    username_field = ft.TextField(
        label="User name",
        hint_text="Enter your user name",
        helper_text="This is your unique identifier",
        width=300,
        autofocus=True,
        icon=ft.Icons.PERSON,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
    )

    password_field = ft.TextField(
        label="Password",
        hint_text="Enter your password",
        helper_text="This is your secret key",
        width=300,
        password=True,
        can_reveal_password=True,
        icon=ft.Icons.PASSWORD,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
    )

    # Function to show a dialog
    def show_dialog(title, content, icon_name, icon_color):
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, text_align=ft.TextAlign.CENTER),
            content=ft.Text(content, text_align=ft.TextAlign.CENTER),
            icon=ft.Icon(name=icon_name, color=icon_color),
            actions=[ft.TextButton("OK", on_click=close_dialog)],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Function to close dialogs
    def close_dialog(e):
        page.dialog.open = False
        page.update()

    # Login logic
    def login_click(e):
        username = username_field.value
        password = password_field.value

        # Input validation
        if not username or not password:
            show_dialog(
                title='Input Error',
                content='Please enter username and password',
                icon_name=ft.Icons.INFO,
                icon_color='blue'
            )
            return

        # Database authentication
        connection = None
        try:
            connection = connect_db()
            cursor = connection.cursor()
            
            # Use a parameterized query to prevent SQL injection
            query = "SELECT username FROM users WHERE username = %s AND password = %s"
            
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                show_dialog(
                    title='Login Successful',
                    content=f'Welcome, {username}!',
                    icon_name=ft.Icons.CHECK_CIRCLE,
                    icon_color='green'
                )
            else:
                show_dialog(
                    title='Login Failed',
                    content='Invalid username or password',
                    icon_name=ft.Icons.ERROR,
                    icon_color='red'
                )

        except Error as err:
            show_dialog(
                title='Database Error',
                content='An error occurred while connecting to the database',
                icon_name=ft.Icons.WARNING,
                icon_color='orange'
            )
        finally:
            if connection and connection.is_connected():
                connection.close()

    # Login button
    login_button = ft.ElevatedButton(
        text="Login",
        on_click=login_click,
        width=100,
        icon=ft.Icons.LOGIN,
    )

    # Main content layout
    main_column = ft.Column(
        controls=[
            login_title,
            username_field,
            password_field,
            ft.Row(
                controls=[login_button],
                alignment=ft.MainAxisAlignment.END,
                width=300
            )
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Container for centering and background
    main_container = ft.Container(
        content=main_column,
        padding=30,
        alignment=ft.alignment.center,
        expand=True
    )
    
    page.add(main_container)

# Start the Flet application
ft.app(target=main)