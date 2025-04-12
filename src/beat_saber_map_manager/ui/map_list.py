from typing import cast
from itertools import batched

import flet as ft

from beat_saber_map_manager.data.map_detail import Difficulty
from beat_saber_map_manager.data.maps import BSMap
from beat_saber_map_manager.ui.map_detail import MapDetailUI


class MapListUI:
    def __init__(self, bsmaps: list[BSMap], detail_handle: MapDetailUI) -> None:
        self.content: ft.ListView | None = None
        self.bsmaps = bsmaps
        self.selected_map: str | None =  None
        self.detail_handle = detail_handle

        self._build_content()
    
    def _build_content(self) -> None:
        self.content = ft.ListView(expand=1)

        for bsmap in self.bsmaps:
            tail = self._make_tile_tail(bsmap.detail.difficulties)

            self.content.controls.append(ft.ListTile(
                title=ft.Text(bsmap.detail.song_name),
                subtitle=ft.Text(bsmap.detail.song_author_name),
                on_click=self._on_list_tile_click,
                leading=ft.Icon(ft.Icons.MULTITRACK_AUDIO),
                trailing=ft.Text(tail, text_align=ft.TextAlign.END),
                data=bsmap,
            ))
        
        self._handle_ui_select(cast(list[ft.ListTile], self.content.controls)[0])
    
    @staticmethod
    def _make_tile_tail(lst: list[Difficulty]) -> str:
        match len(lst):
            case 1:
                tail = lst[0].name
            case 2 | 3:
                tail = "\n".join([d.name for d in lst])
            case 4 | 6:
                btch = batched([d.name for d in lst], 2)
                tail = "\n".join([", ".join(d) for d in btch])
            case _:
                btch = batched([d.name for d in lst], 3)
                tail = "\n".join([", ".join(d) for d in btch])
        
        return tail

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
