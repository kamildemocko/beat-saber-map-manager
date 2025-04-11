from typing import Literal

import flet as ft

from beat_sabre_map_manager.ui.map_list import MapListUI
from beat_sabre_map_manager.ui.map_detail import MapDetailUI
from beat_sabre_map_manager.ui.bottom_actions import BottomActionsUI
from beat_sabre_map_manager.ui.top_actions import TopActionsUI
from beat_sabre_map_manager.data.maps import Maps
from beat_sabre_map_manager.data.bspath import BSPath
from beat_sabre_map_manager.ui.status import StatusUI

class App:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.error = ""

        # set data handle for popups
        status_handle = StatusUI(page)

        # set data handle for maps with details
        game_path, err = BSPath().find_game_path()
        if err != "":
            self.error = err
            return

        self.maps_handle = Maps(game_path)
        self.maps_handle.load_maps()
        self.maps_handle.sort_maps_interpret_asc()

        # set up UI
        self.ui_map_detail = MapDetailUI(status_handle, self.reload_maps)
        self.ui_bottom_actions = BottomActionsUI(game_path, status_handle, self.reload_maps)
        self.ui_top_actions = TopActionsUI(self.reload_maps)
        self.ui_map_list = MapListUI(self.maps_handle.maps, self.ui_map_detail)

        # main containers
        self.map_list_container = ft.Container(
            content=self.ui_map_list.content,
            height=530,
            border=ft.border.all(2, ft.Colors.PRIMARY),
            border_radius=8
        )
        
        self.map_detail_container = ft.Container(
            content=self.ui_map_detail.content,
            height=300,
            border=ft.border.all(2, ft.Colors.PRIMARY),
            border_radius=8,
        )
        
        self.bottom_actions_container = ft.Container(
            content=self.ui_bottom_actions.content,
        )

        self.top_actions_container = ft.Container(
            content=self.ui_top_actions.content,
        )
    
    def reload_maps(
        self, 
        sorting: Literal["interpret_asc", "interpret_desc", "song_asc", "song_desc"] = "interpret_asc"
    ) -> None:
        self.maps_handle.reload_maps()
        match sorting:
            case "interpret_desc":
                self.maps_handle.sort_maps_interpret_asc(reverse=True)
            case "song_asc":
                self.maps_handle.sort_maps_song_asc()
            case "song_desc":
                self.maps_handle.sort_maps_song_asc(reverse=True)
            case _: 
                self.maps_handle.sort_maps_interpret_asc()

        self.ui_map_list = MapListUI(self.maps_handle.maps, self.ui_map_detail)
        self.map_list_container.content = self.ui_map_list.content

        self.page.update()

    def build_ui(self, page: ft.Page) -> None:
        if self.error != "":
            page.add(
                ft.Row([
                    ft.Column([
                        ft.Icon(ft.Icons.ERROR, size=80),
                        ft.Text("Error!", size=40, weight=ft.FontWeight.BOLD),
                        ft.Text(self.error, size=20),
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ], alignment=ft.MainAxisAlignment.CENTER, expand=1),
            )
        else:
            page.add(ft.Column([self.top_actions_container]))
            page.add(ft.Column([self.map_list_container]))
            page.add(ft.Column([self.map_detail_container]))
            page.add(ft.Column([self.bottom_actions_container]))
