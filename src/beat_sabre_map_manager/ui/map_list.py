from pathlib import Path
from typing import cast

import flet as ft

from beat_sabre_map_manager.data.maps import BSMap
from beat_sabre_map_manager.ui.map_detail import MapDetailUI


class MapListUI:
    def __init__(self, bsmaps: list[BSMap], detail_handle: MapDetailUI) -> None:
        self.content: ft.ListView | None = None
        self.bsmaps = bsmaps
        self.selected_map: str | None =  None
        self.detail_handle = detail_handle

        self._build_content()
    
    def update_maps(self, bsmaps: list[Path]) -> None:
        # TODO use
        self.bsmaps = bsmaps

    def _build_content(self) -> None:
        self.content = ft.ListView(expand=1)

        for bsmap in self.bsmaps:
            self.content.controls.append(ft.ListTile(
                title=ft.Text(bsmap.name),
                on_click=self._on_list_tile_click,
                data=bsmap,
            ))

    def _on_list_tile_click(self, e: ft.ControlEvent) -> None:
        if self.content is None:
            return
        
        for item in self.content.controls:
            item = cast(ft.ListTile, item)
            item.bgcolor = None
            item.text_color = None
            cast(ft.Text, item.title).weight = ft.FontWeight.NORMAL
        
        e.control = cast(ft.ListTile, e.control)
        e.control.bgcolor = ft.Colors.BLUE_200
        e.control.text_color = ft.Colors.BLUE_900
        cast(ft.Text, e.control.title).weight = ft.FontWeight.BOLD

        self.selected_map = cast(ft.Text, e.control.title).value

        map_data = cast(BSMap, e.control.data)
        self.detail_handle.build_content(map_data.detail)

        self.content.update()
