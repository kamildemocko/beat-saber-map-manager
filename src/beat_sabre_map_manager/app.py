import flet as ft

from beat_sabre_map_manager.ui.map_list import MapList

class App:
    def __init__(self) -> None:
        self.map_list: MapList = MapList()

    def build_ui(self, page: ft.Page) -> None:
        page.add(ft.Column([
            ft.Markdown("# Map Name:"),
            ft.Container(
                content=self.map_list.content,
                height=400,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=8
            )
        ]))
