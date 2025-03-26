from typing import cast

import flet as ft


class MapList:
    def __init__(self) -> None:
        self.content: ft.ListView | None = None
        self.selected_map: str | None =  None

        self._build_map_list()

    def _build_map_list(self) -> None:
        self.content = ft.ListView(expand=1)

        for i in range(20):
            name = f"item {i}"
            self.content.controls.append(ft.ListTile(
                title=ft.Text(name),
                on_click=self._on_list_tile_click
            ))

    def _on_list_tile_click(self, e: ft.ControlEvent) -> None:
        if self.content is None:
            return
        
        for item in self.content.controls:
            item = cast(ft.ListTile, item)
            item.bgcolor = None
            item.text_color = None
        
        e.control = cast(ft.ListTile, e.control)
        e.control.bgcolor = ft.Colors.BLUE_200
        e.control.text_color = ft.Colors.BLUE_900

        self.selected_map = cast(ft.Text, e.control.title).value
        self.content.update()
