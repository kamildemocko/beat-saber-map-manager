import flet as ft
import importlib.metadata

VERSION = importlib.metadata.version("beat_saber_map_manager")

class StatusUI:
    """A class to manage the status UI of the application."""
    def __init__(self, page: ft.Page) -> None:
        self.page = page

    def pop(self, value: str) -> None:
        self.page.open(ft.SnackBar(
            content=ft.Text(value, weight=ft.FontWeight.BOLD),
            show_close_icon=True,
        ))