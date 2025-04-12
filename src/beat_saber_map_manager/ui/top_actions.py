from typing import Callable

import flet as ft


class TopActionsUI:
    def __init__(
        self, 
        map_reload_callback: Callable
    ) -> None:
        self.map_reload_callback = map_reload_callback

        self.content = ft.Container(
            content=ft.Row([]),
            padding=16,
        )

        self.build_content()

    def build_content(self) -> None:
        col = ft.Column([
            ft.Row([
                ft.SegmentedButton(segments=[
                    ft.Segment(value="interpret_asc", label=ft.Text("Interpret A - Z")),
                    ft.Segment(value="interpret_desc", label=ft.Text("Interpret Z - A")),
                    ft.Segment(value="song_asc", label=ft.Text("Song A - Z")),
                    ft.Segment(value="song_desc", label=ft.Text("Song Z - A")),
                ], selected={"interpret_asc"}, on_change=self._handle_change, expand=1)
            ], alignment=ft.MainAxisAlignment.CENTER)
        ])

        self.content = col
    
    def _handle_change(self, e: ft.ControlEvent):
        if e.data is None:
            return

        self.map_reload_callback(sorting=e.data[2:-2])
    