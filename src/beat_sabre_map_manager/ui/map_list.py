from pathlib import Path
from typing import cast

import flet as ft

from beat_sabre_map_manager.data.maps import BSMap


class MapList:
    def __init__(self, bsmaps: list[BSMap]) -> None:
        self.content: ft.ListView | None = None
        self.bsmaps = bsmaps
        self.selected_map: str | None =  None

        self._build_map_list()
    
    def update_maps(self, bsmaps: list[Path]) -> None:
        self.bsmaps = bsmaps

    def _build_map_list(self) -> None:
        self.content = ft.ListView(expand=1)

        for bsmap in self.bsmaps:
            self.content.controls.append(ft.ListTile(
                title=ft.Text(bsmap.name),
                on_click=self._on_list_tile_click
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
        self.content.update()
