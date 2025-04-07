import flet as ft

from beat_sabre_map_manager.ui.map_list import MapListUI
from beat_sabre_map_manager.ui.map_detail import MapDetailUI
from beat_sabre_map_manager.ui.bottom_actions import BottomActionsUI
from beat_sabre_map_manager.data.maps import Maps
from beat_sabre_map_manager.ui.status import StatusUI

class App:
    def __init__(self, page: ft.Page) -> None:
        self.page = page

        # set data handle for popups
        status_handle = StatusUI(page)

        # set data handle for maps with details
        maps_handle = Maps()
        maps_handle.load_maps()
        maps_handle.sort_maps_asc()

        # set up UI
        self.ui_map_detail = MapDetailUI(status_handle)
        self.ui_map_list = MapListUI(maps_handle.maps, self.ui_map_detail)
        self.ui_bottom_actions = BottomActionsUI(status_handle)

    def build_ui(self, page: ft.Page) -> None:
        page.add(ft.Column([
            ft.Container(
                content=self.ui_map_list.content,
                height=400,
                border=ft.border.all(2, ft.Colors.BLUE_200),
                border_radius=8
            )
        ]))

        page.add(ft.Column([
            ft.Container(
                content=self.ui_map_detail.content,
                height=300,
                border=ft.border.all(2, ft.Colors.BLUE_200),
                border_radius=8,
            )
        ]))

        page.add(ft.Column([
            ft.Container(
                content=self.ui_bottom_actions.content,
            )
        ]))
