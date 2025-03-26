import flet as ft

from beat_sabre_map_manager.ui.map_list import MapList
from beat_sabre_map_manager.data.maps import Maps

class App:
    def __init__(self) -> None:
        maps_handle = Maps()
        maps_handle.load_maps()
        self.map_list: MapList = MapList(maps_handle.maps)

    def build_ui(self, page: ft.Page) -> None:
        # page.add(ft.Column([
        #     ft.Container(
        #         content=ft.Row([ft.Markdown("drop your custom map here to add it to the game")], expand=1, alignment=ft.MainAxisAlignment.CENTER),
        #         height=100,
        #     ),
        #     ft.Divider(thickness=.4, color=ft.Colors.GREY_300),
        # ]))

        page.add(ft.Column([
            ft.Markdown("# Map Name:"),
            ft.Container(
                content=self.map_list.content,
                height=400,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=8
            )
        ]))
