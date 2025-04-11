from typing import cast

import flet as ft

from beat_sabre_map_manager.data.maps import BSMap
from beat_sabre_map_manager.ui.map_detail import MapDetailUI


class MapListUI:
    def __init__(self, bsmaps: list[BSMap], detail_handle: MapDetailUI, sorting: str) -> None:
        self.content: ft.ListView | None = None
        self.bsmaps = bsmaps
        self.selected_map: str | None =  None
        self.detail_handle = detail_handle
        self.sorting = sorting

        self._build_content()
    
    def _build_content(self) -> None:
        self.content = ft.ListView(expand=1)

        for bsmap in self.bsmaps:
            if self.sorting.startswith("interpret"):
                tile_title = f"{bsmap.detail.song_author_name} ◆ {bsmap.detail.song_name}"
            else:
                tile_title = f"{bsmap.detail.song_name} ◆ {bsmap.detail.song_author_name}"

            self.content.controls.append(ft.ListTile(
                title=ft.Text(tile_title),
                on_click=self._on_list_tile_click,
                leading=ft.Icon(ft.Icons.MULTITRACK_AUDIO),
                data=bsmap,
            ))
        
        self._handle_ui_select(cast(list[ft.ListTile], self.content.controls)[0])
    
    def _handle_ui_select(self, selected_tile: ft.ListTile) -> None:
        if self.content is None:
            return

        for item in self.content.controls:
            item = cast(ft.ListTile, item)
            item.bgcolor = None
            item.text_color = None
            cast(ft.Text, item.title).weight = ft.FontWeight.NORMAL
            cast(ft.Icon, item.leading).color = ft.Colors.WHITE

        selected_tile.bgcolor = ft.Colors.PRIMARY
        selected_tile.text_color = ft.Colors.BLACK
        cast(ft.Text, selected_tile.title).weight = ft.FontWeight.BOLD
        cast(ft.Icon, selected_tile.leading).color = ft.Colors.BLACK

        map_data = cast(BSMap, selected_tile.data)
        self.detail_handle.build_content(map_data)

    def _on_list_tile_click(self, e: ft.ControlEvent) -> None:
        """handle click event on a list tile in the map list, updates visual state of tiles and trings detail view
        Args:
            e (ft.ControlEvent): The click event containing the control that was clicked.
        """
        if self.content is None:
            return
        
        if self.selected_map == cast(ft.Text, e.control.title).value:
            # same map as selected
            return
        
        self._handle_ui_select(e.control)
        self.selected_map = cast(ft.Text, e.control.title).value
        self.content.update()
