import flet as ft

from beat_sabre_map_manager.ui.map_list import MapListUI
from beat_sabre_map_manager.ui.map_detail import MapDetailUI
from beat_sabre_map_manager.ui.bottom_actions import BottomActionsUI
from beat_sabre_map_manager.data.maps import Maps

class App:
    def __init__(self) -> None:
        maps_handle = Maps()
        maps_handle.load_maps()
        self.map_detail = MapDetailUI()
        self.map_list = MapListUI(maps_handle.maps, self.map_detail)
        self.bottom_actions = BottomActionsUI()

    def build_ui(self, page: ft.Page) -> None:
        # page.add(ft.Column([
        #     ft.Container(
        #         content=ft.Row([ft.Markdown("drop your custom map here to add it to the game")], expand=1, alignment=ft.MainAxisAlignment.CENTER),
        #         height=100,
        #     ),
        #     ft.Divider(thickness=.4, color=ft.Colors.GREY_300),
        # ]))

        page.add(ft.Column([
            ft.Container(
                content=self.map_list.content,
                height=400,
                border=ft.border.all(2, ft.Colors.BLUE_200),
                border_radius=8
            )
        ]))

        page.add(ft.Column([
            ft.Container(
                content=self.map_detail.content,
                height=300,
                border=ft.border.all(2, ft.Colors.BLUE_200),
                border_radius=8,
            )
        ]))

        page.add(ft.Column([
            ft.Container(
                content=self.bottom_actions.content,
            )
        ]))
